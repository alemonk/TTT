from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from . import db
from flask_login import login_user, login_required, current_user

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

        return redirect(url_for('views.quick_test'))

    return render_template("settings.html", user=current_user)


@settings.route('/get_preferences', methods=['POST'])
@login_required
def get_preferences():
    # Retrieve the current user from the database
    user = User.query.get(current_user.id)

    num_open_q = user.open_question_pref
    num_tf_q = user.true_or_false_pref
    num_closed_q = user.closed_question_pref

    print(num_closed_q)
    print(num_tf_q)
    print(num_closed_q)

    return jsonify({'num_open_q': num_open_q, 'num_tf_q': num_tf_q, 'num_closed_q': num_closed_q})
