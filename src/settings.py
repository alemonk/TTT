from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from .models import User
from . import db
from flask_login import login_required, current_user

settings = Blueprint('settings', __name__)


@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def save_settings():
    print('\n\nSave settings route called')
    if request.method == 'POST':
        numOpenQuestions = request.form.get('numOpenQuestions')
        numTrueFalseQuestions = request.form.get('numTrueFalseQuestions')
        numClosedQuestions = request.form.get('numClosedQuestions')

        # Retrieve the current user from the database
        user = User.query.get(current_user.id)

        # Update the user's preferences
        user.open_question_pref = numOpenQuestions
        user.true_or_false_pref = numTrueFalseQuestions
        user.closed_question_pref = numClosedQuestions

        db.session.commit()
        flash('Your Settings Have Been Successfully Updated', category='success')

    return render_template("settings.html", user=current_user)


@settings.route('/get_preferences', methods=['POST'])
@login_required
def get_preferences():
    # Retrieve the current user from the database
    user = User.query.get(current_user.id)

    num_open_q = user.open_question_pref
    num_tf_q = user.true_or_false_pref
    num_closed_q = user.closed_question_pref

    return jsonify({'num_open_q': num_open_q, 'num_tf_q': num_tf_q, 'num_closed_q': num_closed_q})


# Define a route to handle language selection
@settings.route('/language', methods=['GET', 'POST'])
def change_language():
    if request.method == 'POST':
        # Get the selected language from the request
        data = request.get_json()
        lang = data['language']

        # Check if the user is logged in
        if current_user.is_authenticated:
            # Retrieve the current user from the database
            user = User.query.get(current_user.id)

            # Update the user's language preference in the database
            user.language = lang
            db.session.commit()
        else:
            # Update the language preference in the session
            session['language'] = lang

        # Return a success message
        return jsonify({'success': True})


@settings.route('/get_language', methods=['GET'])
def get_language():
    # Check if the user is logged in
    if current_user.is_authenticated:
        # Retrieve the current user from the database
        user = User.query.get(current_user.id)

        # Return the user's language preference as a JSON object
        return jsonify({'language': user.language})
    else:
        # Return the language preference from the session as a JSON object
        return jsonify({'language': session.get('language')})
