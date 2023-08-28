from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Test
from . import db
import json

history = Blueprint('history', __name__)


# Route for viewing past tests
@history.route('/history', methods=['GET', 'POST'])
@login_required
def show_old_tests():
    print('\n\nHistory route called')
    print(current_user.tests)
    # Render notes template on GET request
    return render_template("history.html", user=current_user)


# Route for deleting a test
@history.route('/delete-test', methods=['POST'])
@login_required
def delete_test():
    print('\n\nDeleting a test')
    # Get note ID from request data
    test_id = json.loads(request.data)['testId']

    # Query database for note with given ID
    test = Test.query.get(test_id)

    # Check if note exists and belongs to current user
    if test and test.user_id == current_user.id:
        # Delete note from database and return success response
        db.session.delete(test)
        db.session.commit()
        return jsonify({'success': True})

    # Return failure response if note does not exist or does not belong to current user
    return jsonify({'success': False})


# Route for showing a test
@history.route('/get-test', methods=['POST'])
@login_required
def get_test_data():
    print('\n\nShowing a test')
    # Get test ID from form data
    test_id = request.form.get('test_id')

    # Query database for test with given ID
    test = Test.query.get(test_id)

    # Check if test exists and belongs to current user
    if not test or test.user_id != current_user.id:
        return jsonify({'error': 'Test not found'})

    # Return test questions and answers as JSON response
    return jsonify({'questions': test.questions, 'answers': test.answers})
