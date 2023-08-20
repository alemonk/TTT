from flask import Blueprint, jsonify, request
from flask_login import current_user
from sqlalchemy import func
from .create_random_question import create_random_question
from .models import Note
from .open_question_check import open_question_check

questions = Blueprint('questions', __name__)


@questions.route('/question', methods=['POST'])
def get_question():
    difficulty = request.json['difficulty']
    type_of_question = request.json['type_of_question']

    random_note = Note.query.filter_by(user_id=current_user.id).order_by(func.random()).first()
    if random_note:

        question, answer = create_random_question(random_note.data,
                                                  type_of_question=type_of_question,
                                                  difficulty=difficulty)

        # Normalize the value of answer for true or false questions
        if type_of_question == 'true or false':
            if answer.lower().startswith('true') or answer.startswith('1'):
                answer = 'True'
            elif answer.lower().startswith('false') or answer.startswith('0'):
                answer = 'False'
        elif type_of_question == 'closed question':
            # Normalize the value of answer
            if answer.upper().startswith('A'):
                answer = 'A'
            elif answer.upper().startswith('B'):
                answer = 'B'
            elif answer.upper().startswith('C'):
                answer = 'C'
            elif answer.upper().startswith('D'):
                answer = 'D'

        # Print the values of question and answer for debugging
        print(f'question: {question}')
        print(f'answer: {answer}')

        return jsonify({'question': question, 'answer': answer})
    else:
        return jsonify({'question': "No notes available.", 'answer': ""})


@questions.route('/check_open_question', methods=['POST'])
def check_open_question():
    data = request.get_json()
    guess = data['guess']
    question = data['question']
    answer = data['answer']
    response = open_question_check(guess, question, answer)

    # Print the value of response for debugging
    print(response)

    return jsonify({'response': response})
