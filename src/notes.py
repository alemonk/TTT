from flask import Blueprint, render_template, request, jsonify, flash, send_file
from flask_login import login_required, current_user
from .models import Note, Folder
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
        folder_id = request.form.get('folder_id')

        # Extract content from file data
        content = unpack_file(data)

        # Create new note object and add it to the database
        new_note = Note(title=title, data=data, content=content, user_id=current_user.id, folder_id=folder_id)
        db.session.add(new_note)
        db.session.commit()

        print('\n\nNote: ' + title + ' added!')
        flash('Note successfully added!', category='success')
        return jsonify({'success': True})

    # Render notes template on GET request
    return render_template("notes.html", user=current_user)


# Helper function to extract content from file data
def unpack_file(data, file_type=None):

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
        # # If PyPDF2 fails to extract any text, use Tesseract OCR to extract text from PDF file
        # if not content:
        #    images = convert_from_bytes(data)
        #    for image in images:
        #        content += pytesseract.image_to_string(image)

    elif file_type == 'image':
        # Extract text from image using Tesseract OCR
        with io.BytesIO(data) as data_stream:
            image = Image.open(data_stream)
            content = pytesseract.image_to_string(image)

    print('content: ', content)
    return content


# Route for opening a note
# TODO open also other kind of files
@notes.route('/open-note/<int:note_id>', methods=['GET'])
@login_required
def open_note(note_id):
    # Query database for note with given ID
    note = Note.query.get(note_id)

    # Check if note exists and belongs to current user
    if not note or note.user_id != current_user.id:
        return jsonify({'error': 'Note not found'})

    # Create a BytesIO object from the PDF data
    pdf_io = io.BytesIO(note.data)

    # Send the PDF data as a response
    return send_file(pdf_io, mimetype='application/pdf')


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
        flash('Note successfully deleted!', category='success')
        return jsonify({'success': True})

    # Return failure response if note does not exist or does not belong to current user
    return jsonify({'success': False})


# Route for creating a folder
@notes.route('/folders', methods=['POST'])
@login_required
def create_folder():
    print('\n\nFolders route called')

    # Get folder title and file data from form
    data = request.get_json()
    folder_title = data['title']

    # Create new note object and add it to the database
    new_folder = Folder(title=folder_title, user_id=current_user.id)
    db.session.add(new_folder)
    db.session.commit()

    print('\n\nNote: ' + folder_title + ' added!')
    flash('Folder successfully created!', category='success')
    return jsonify({'success': True})


@notes.route('/delete-folder', methods=['POST'])
@login_required
def delete_folder():
    # Get folder ID from request data
    folder_id = json.loads(request.data)['folderId']

    # Query database for folder with given ID
    folder = Folder.query.get(folder_id)

    # Check if folder exists and belongs to current user
    if folder and folder.user_id == current_user.id:
        # Delete all notes associated with the folder
        for note in folder.notes:
            db.session.delete(note)

        # Delete the folder from the database
        db.session.delete(folder)
        db.session.commit()

        flash('Folder successfully deleted!', category='success')
        return jsonify({'success': True})

    # Return failure response if folder does not exist or does not belong to current user
    return jsonify({'success': False})


@notes.route('/rename_folder', methods=['POST'])
@login_required
def rename_folder():
    data = request.get_json()
    folder_id = data['id']
    new_title = data['title']

    folder = Folder.query.get(folder_id)
    if folder.user_id == current_user.id:
        folder.title = new_title
        db.session.commit()

        flash('Folder successfully renamed!', category='success')
        return jsonify({'success': True})

    flash('Failed to rename the folder', category='error')
    return jsonify({'success': False})


@notes.route('/rename_folder_description', methods=['POST'])
@login_required
def rename_folder_description():
    data = request.get_json()
    folder_id = data['id']
    new_description = data['description']

    folder = Folder.query.get(folder_id)
    if folder.user_id == current_user.id:
        folder.description = new_description
        db.session.commit()

        flash('Folder description successfully changed!', category='success')
        return jsonify({'success': True})

    flash('Failed to change the folder description', category='error')
    return jsonify({'success': False})
