from openai import OpenAI
from .openai_key import openai_key

client = OpenAI(api_key=openai_key)
import backoff
import random
import re
import logging
import os
from .utils.prompt_openai import prompt_openai
from .utils.prompt_user import prompt_user
from .models import User
from flask_login import current_user
from openai._exceptions import RateLimitError, OpenAIError

logging.basicConfig(level=logging.INFO)

# Set your OpenAI API key
openai_key = os.getenv('api_key')


def log_backoff(details):
    logging.info(f"Backing off {details['wait']} seconds after {details['tries']} tries")


@backoff.on_exception(
    backoff.constant,
    (RateLimitError, OpenAIError),  # OpenAIError replaces ServiceUnavailableError
    max_tries=10,
    on_backoff=log_backoff,
    interval=10
)
def get_openai_response_with_backoff(prompt_question, system_content):
    print('\n\nrequest to openai with backoff')

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": system_content},
              {"role": "user", "content": prompt_question}],
    temperature=0.8,
    frequency_penalty=0.3,
    presence_penalty=0.8)
    print('\n\nresponse: ' + str(response))
    response = response.choices[0].message.content

    return response


def create_random_question(note, type_of_question='true or false'):
    # Get preferred language
    user = User.query.get(current_user.id)
    language = user.language
    print('language: ' + str(language))

    # Set up the prompt for openAI API
    truncated_note = select_random_note_portion(note, max_note_length=750)
    prompt_question = prompt_user(language, truncated_note)
    system_content = prompt_openai(language, type_of_question)

    print('\n\nPrompt question: ' + prompt_question)

    # Generate ai response
    ai_output = get_openai_response_with_backoff(prompt_question, system_content)
    print('\n\nai_output: ' + ai_output)

    # Split AI generated output into question and answer
    [question, answer] = split_string(ai_output)

    # Check if generated question is valid
    is_valid = check_question_validity(question, answer, type_of_question)

    # If generated question is not valid, generate a new one
    while not is_valid:
        truncated_note = select_random_note_portion(note, max_note_length=750)
        prompt_question = "Ask one random question using a few sentences from the following: " + truncated_note
        ai_output = get_openai_response_with_backoff(prompt_question, system_content)
        #print('\n\nAI response: ' + ai_output)
        [question, answer] = split_string(ai_output)
        is_valid = check_question_validity(question, answer, type_of_question)

    # Return valid question and answer
    return [question, answer]


def select_random_note_portion(note, max_note_length):
    print('Note length: ' + str(len(note)))
    # Truncate note if it's longer than max_note_length
    if len(note) > max_note_length:
        start_idx = random.randint(0, len(note) - max_note_length)
        truncated_note = note[start_idx:start_idx + max_note_length]
    else:
        # If the note is very short, then consider only a small portion
        truncated_note = select_random_note_portion(note, max_note_length/2)

    print('Selected portions length: ' + str(len(truncated_note)))
    return truncated_note


def check_question_validity(question: str, answer: str, type_of_question: str) -> bool:
    # Check if rpm are too many
    if question == 'A LOT of people are using this app, what do you say? ':
        return True

    # Check if the question is a valid true or false question
    if type_of_question == 'true or false':
        if answer.split('.')[0].strip() not in ['TRUE', 'FALSE', 'True', 'False', 'true', 'false']:
            print('\n\nQuestion not valid. Regenerate...')
            return False

    # Check if the question is a valid-closed question
    if type_of_question == 'closed question':
        options = re.findall(r'\b[A-D]\)', question)
        if len(options) < 2:
            print('\n\nQuestion not valid. Regenerate...')
            return False

    # If all checks passed, return True
    print('\n\nValid question!')
    return True


def split_string(input_string: str) -> list:
    try:
        question = re.split(r'QUESTION:\s*', input_string)[1].split('CORRECT ANSWER:')[0]
        answer = re.split(r'CORRECT ANSWER:\s*', input_string)[1]
        return [question, answer]
    except Exception as e:
        print(f"\n\nAn error occurred while splitting the AI output: {e}")
        return [input_string, ""]
