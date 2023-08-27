from flask import Blueprint, jsonify, request
from flask_login import current_user
from sqlalchemy import func
from .create_random_question import create_random_question
from .models import Note, Test
from .check_answer import check_answer
from . import db

questions = Blueprint('questions', __name__)


@questions.route('/question', methods=['POST'])
def get_question():
    type_of_question = request.json['type_of_question']

    random_note = Note.query.filter_by(user_id=current_user.id).order_by(func.random()).first()

    question, answer = create_random_question(random_note.content,
                                              type_of_question=type_of_question)

    answer = normalize_answer(type_of_question, answer)

    # Print the values of question and answer for debugging
    print(f'\n\nquestion: {question}')
    print(f'answer: {answer}')

    # Return the question, answer, and type of question as a JSON object
    return jsonify({'question': question, 'answer': answer, 'type_of_question': type_of_question})


@questions.route('/open_question_check_answer', methods=['POST'])
def check_open_question():
    data = request.get_json()
    guess = data['guess']
    question = data['question']
    answer = data['answer']
    response = check_answer(guess, question, answer)

    # Print the value of response for debugging
    print('\n\nresponse: ' + response)

    return jsonify({'response': response})


@questions.route('/true_or_false_check_answer', methods=['POST'])
def true_or_false_check_answer():
    data = request.get_json()
    guess = data['guess']
    question = data['question']
    answer = data['answer']

    if answer.startswith(guess):
        response = f"Correct! {answer}"
    else:
        response = f"Incorrect. The correct answer is {answer}"

    return jsonify({'response': response})


@questions.route('/closed_question_check_answer', methods=['POST'])
def closed_question_check_answer():
    data = request.get_json()
    guess = data['guess']
    question = data['question']
    answer = data['answer']

    if answer.startswith(guess):
        response = f"Correct! {answer}"
    else:
        response = f"Incorrect. The correct answer is {answer}"

    return jsonify({'response': response})


def normalize_answer(type_of_question, answer):
    # Split the answer into words
    words = answer.split()

    # Normalize the value of answer for true or false questions
    if type_of_question == 'true or false':
        if words[0].lower().startswith('true'):
            words[0] = 'True.'
        elif words[0].lower().startswith('false'):
            words[0] = 'False.'

    elif type_of_question == 'closed question':
        # Normalize the value of answer
        if words[0].upper().startswith('A'):
            words[0] = 'A'
        elif words[0].upper().startswith('B'):
            words[0] = 'B'
        elif words[0].upper().startswith('C'):
            words[0] = 'C'
        elif words[0].upper().startswith('D'):
            words[0] = 'D'

    # Join the words back into a single string
    answer = ' '.join(words)
    return answer


@questions.route('/save_test_in_database', methods=['POST'])
def save_test_in_database():
    try:
        # Get the data sent from the client
        user_guesses = request.get_json()

        # Create lists to store the data
        generated_questions = []
        user_guesses_list = []
        type_of_question_list = []
        correct_answer_list = []

        # Iterate over the user_guesses array
        for obj in user_guesses:
            # Access the properties of each object in the user_guesses array
            question = obj['question']
            guess = obj['guess']
            type_of_question = obj['type_of_question']
            correct_answer = obj['answer']

            # Add the data to the respective lists
            generated_questions.append(question)
            user_guesses_list.append(guess)
            type_of_question_list.append(type_of_question)
            correct_answer_list.append(correct_answer)

        # Create a new Test object
        test = Test()
        test.questions = generated_questions
        test.guesses = user_guesses_list
        test.question_types = type_of_question_list
        test.answers = correct_answer_list

        # Associate the Test object with the current user
        test.user_id = current_user.id

        # Add the new Test object to the database session
        db.session.add(test)
        # Commit the changes to save the Test object to the database
        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
