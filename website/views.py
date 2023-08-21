from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/notes', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form.get('title')
        data = request.form.get('data')

        if len(data) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(title=title, data=data, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            print('Note: ' + title + ' added!')
            return jsonify({'id': new_note.id, 'title': title})

    return render_template("notes.html", user=current_user)


@views.route('/note-content', methods=['POST'])
@login_required
def get_note_content():
    note_id = request.form.get('note_id')
    note = Note.query.get(note_id)
    if not note or note.user_id != current_user.id:
        return jsonify({'error': 'Note not found'})
    return note.data


@views.route('/delete-note', methods=['DELETE'])
@login_required
def delete_note():
    note_id = json.loads(request.data)['noteId']
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})