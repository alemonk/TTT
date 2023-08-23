import io
import PyPDF2
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


# Route for creating and viewing notes
@views.route('/notes', methods=['GET', 'POST'])
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
def unpack_file(data):
    # Convert data to byte string if necessary
    if isinstance(data, str):
        data = data.encode()

    # Determine the file type based on its contents
    file_type = None
    if data.startswith(b'%PDF-'):
        file_type = 'pdf'
    else:
        file_type = 'txt'

    # Extract the content from the file based on its type
    content = None
    if file_type == 'pdf':
        # Extract text from PDF file
        with io.BytesIO(data) as data_stream:
            reader = PyPDF2.PdfReader(data_stream)
            content = ''
            for page in range(len(reader.pages)):
                content += reader.pages[page].extract_text()
    elif file_type == 'txt':
        # Extract text from txt file
        content = data.decode()
    return content


# Route for getting note content
@views.route('/note-content', methods=['POST'])
@login_required
def get_note_content():
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
@views.route('/delete-note', methods=['POST'])
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


# Route for quiz feature (not implemented)
@views.route('/quiz_me')
@login_required
def quiz_me():
    print('\n\nQuizMe route called')
    return render_template("quiz_me.html", user=current_user)


# Route for personalized test feature (not implemented)
@views.route('/personalized_test')
@login_required
def personalized_test():
    print('\n\nPersonalized test route called')
    return render_template("personalized_test.html", user=current_user)
