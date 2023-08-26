from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

settings = Blueprint('settings', __name__)


@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def save_settings():
    print('\n\nSave settings route called')
    if request.method == 'POST':
        numOpenQuestions = request.form.get('numOpenQuestions')
        numTrueFalseQuestions = request.form.get('numTrueFalseQuestions')
        numClosedQuestions = request.form.get('numClosedQuestions')

        user = User()
        user.open_question_pref = numOpenQuestions
        user.true_or_false_pref = numTrueFalseQuestions
        user.closed_question_pref = numClosedQuestions

        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash('Your Settings Have Been Successfully Updated', category='success')

        return redirect((url_for('views.quick_test')))

    return render_template("settings.html", user=current_user)

