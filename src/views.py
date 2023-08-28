from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


# Route for single question
@views.route('/quiz_me')
@login_required
def quiz_me():
    print('\n\nQuizMe route called')
    return render_template("quiz_me.html", user=current_user)


# Route for quick test
@views.route('/quick_test')
@login_required
def quick_test():
    print('\n\nQuick test route called')
    return render_template("quick_test.html", user=current_user)


# Route for personalized test feature
@views.route('/personalized_test')
@login_required
def personalized_test():
    print('\n\nPersonalized test route called')
    return render_template("personalized_test.html", user=current_user)


