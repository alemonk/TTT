from flask import Blueprint, jsonify, request
from flask_login import current_user
from .models import Note
from sqlalchemy import func
from .question_generator import question_generator
from .open_question_check import open_question_check

questions = Blueprint('questions', __name__)


@questions.route('/open_question')
def open_question():
    random_note = Note.query.filter_by(user_id=current_user.id).order_by(func.random()).first()
    if random_note:
        question, answer = question_generator(random_note.data,
                                              type_of_question='open question',
                                              difficulty='medium')

        # Print the values of question and answer for debugging
        print(f'question: {question}')
        print(f'answer: {answer}')

        return jsonify({'question': question, 'answer': answer})
    else:
        return jsonify({'question': "No notes available.", 'answer': ""})


@questions.route('/true_false_question')
def true_false_question():
    random_note = Note.query.filter_by(user_id=current_user.id).order_by(func.random()).first()
    if random_note:
        question, answer = question_generator(random_note.data,
                                              type_of_question='true or false',
                                              difficulty='medium')
        # Normalize the value of answer
        if answer.lower() in ['true', 't', '1']:
            answer = 'True'
        elif answer.lower() in ['false', 'f', '0']:
            answer = 'False'

        # Print the values of question and answer for debugging
        print(f'question: {question}')
        print(f'answer: {answer}')

        return jsonify({'question': question, 'answer': answer})
    else:
        return jsonify({'question': "No notes available.", 'answer': ""})


@questions.route('/closed_question')
def closed_question():
    random_note = Note.query.filter_by(user_id=current_user.id).order_by(func.random()).first()
    if random_note:
        question, answer = question_generator(random_note.data,
                                              type_of_question='closed question with four possible answers, A, B, C, D',
                                              difficulty='medium')
        # Normalize the value of answer
        answer = answer.upper()
        if 'A' in answer:
            answer = 'A'
        elif 'B' in answer:
            answer = 'B'
        elif 'C' in answer:
            answer = 'C'
        elif 'D' in answer:
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
