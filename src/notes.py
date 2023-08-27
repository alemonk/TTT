from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from pdf2image import convert_from_bytes
from .models import Note
from . import db
import io
import PyPDF2
import json
import pytesseract
from PIL import Image


notes = Blueprint('notes', __name__)


# Route for creating and viewing notes
@notes.route('/notes', methods=['GET', 'POST'])
@login_required
def create_note():
    print('\n\nNotes route called')
    if request.method == 'POST':
        # Get note title and file data from form
        title = request.form.get('title')
        data = request.files['data'].read()

        # Extract content from file data
        content = unpack_file(data)

        # Create new note object and add it to the database
        new_note = Note(title=title, data=data, content=content, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()

        print('\n\nNote: ' + title + ' added!')
        return jsonify({'id': new_note.id, 'title': title})

    # Render notes template on GET request
    return render_template("notes.html", user=current_user)


# Helper function to extract content from file data
def unpack_file(data, file_type=None):
    # Convert data to byte string if necessary
    if isinstance(data, str):
        data = data.encode()

    # Determine the file type based on its contents, the provided file_type parameter, or the file extension
    if not file_type:
        if data.startswith(b'%PDF-'):
            file_type = 'pdf'
        else:
            file_type = 'image'

    # Extract the content from the file based on its type
    content = None
    if file_type == 'pdf':
        # Extract text from PDF file using PyPDF2
        with io.BytesIO(data) as data_stream:
            reader = PyPDF2.PdfReader(data_stream)
            content = ''
            for page in range(len(reader.pages)):
                content += reader.pages[page].extract_text()

        # If PyPDF2 fails to extract any text, use Tesseract OCR to extract text from PDF file
        if not content:
            images = convert_from_bytes(data)
            for image in images:
                content += pytesseract.image_to_string(image)
    elif file_type == 'image':
        # Extract text from image using Tesseract OCR
        with io.BytesIO(data) as data_stream:
            image = Image.open(data_stream)
            content = pytesseract.image_to_string(image)

    return content


# Route for getting note content
@notes.route('/open-note', methods=['POST'])
@login_required
def get_note_data():
    # Get note ID from form data
    note_id = request.form.get('note_id')

    # Query database for note with given ID
    note = Note.query.get(note_id)

    # Check if note exists and belongs to current user
    if not note or note.user_id != current_user.id:
        return jsonify({'error': 'Note not found'})

    # Return note content as JSON response
    return note.content


# Route for deleting a note
@notes.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    # Get note ID from request data
    note_id = json.loads(request.data)['noteId']

    # Query database for note with given ID
    note = Note.query.get(note_id)

    # Check if note exists and belongs to current user
    if note and note.user_id == current_user.id:
        # Delete note from database and return success response
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True})

    # Return failure response if note does not exist or does not belong to current user
    return jsonify({'success': False})
