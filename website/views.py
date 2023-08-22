import io
import PyPDF2
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/notes', methods=['GET', 'POST'])
@login_required
def create_note():
    print('Notes route called')
    if request.method == 'POST':
        title = request.form.get('title')
        data = request.files['data'].read()

        if len(data) < 1:
            flash('Note is too short!', category='error')
        else:
            content = unpack_file(data)
            new_note = Note(title=title, data=data, content=content, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            print('Note: ' + title + ' added!')
            return jsonify({'id': new_note.id, 'title': title})

    return render_template("notes.html", user=current_user)


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


@views.route('/note-content', methods=['POST'])
@login_required
def get_note_content():
    note_id = request.form.get('note_id')
    note = Note.query.get(note_id)
    print(note.content)
    if not note or note.user_id != current_user.id:
        return jsonify({'error': 'Note not found'})
    return note.content


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note_id = json.loads(request.data)['noteId']
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})


@views.route('/quiz_me')
@login_required
def quiz_me():
    print('QuizMe route called')
    return render_template("quiz_me.html", user=current_user)


@views.route('/personalized_test')
@login_required
def personalized_test():
    print('Personalized test route called')
    return render_template("personalized_test.html", user=current_user)
