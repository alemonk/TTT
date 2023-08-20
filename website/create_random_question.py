import openai
import backoff
import random
import re
from website.static.openai_key import openai_key
import logging

logging.basicConfig(level=logging.INFO)

# Set your OpenAI API key
openai.api_key = openai_key()


def log_backoff(details):
    logging.info(f"Backing off {details['wait']} seconds after {details['tries']} tries")


@backoff.on_exception(backoff.expo, openai.error.RateLimitError, max_tries=10, on_backoff=log_backoff, base=5)
def get_openai_response_with_backoff(prompt_question):
    print('request to openai with backoff')

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt_question
        }],
        temperature=0.8,
        frequency_penalty=0.3,
        presence_penalty=0.8,
    )
    return response


def create_random_question(note, type_of_question='true or false', difficulty='medium'):
    # Set up the prompt for openAI API
    truncated_note = select_random_note_portion(note, max_note_length=200)

    prompt_question = "Kind of question: " + type_of_question + \
                      "\nDifficulty: " + difficulty + \
                      "\nAsk one random question using a few sentences from the following:\n" + truncated_note + \
                      "\n\nThe output must be in the format 'QUESTION: [...] ? CORRECT ANSWER: [...] .' " + \
                      "\n\nNote 1: In the case of a 'closed question' there must be A, B, C, or D as possible answers." + \
                      "\nNote 2: The language MUST be the same as the note, which is not necessarily English." + \
                      "\nNote 3: In the case of a 'true or false' question, the answer is TRUE/FALSE regardless of the language."

    # Generate ai response
    response = get_openai_response_with_backoff(prompt_question)
    ai_output = response['choices'][0]['message']['content']
    print('AI response: ' + ai_output)

    # Split AI generated output into question and answer
    [question, answer] = split_string(ai_output)

    # Check if generated question is valid
    is_valid = check_question_validity(question, answer, type_of_question)

    # If generated question is not valid, generate a new one
    while not is_valid:
        response = get_openai_response_with_backoff(prompt_question)
        ai_output = response['choices'][0]['message']['content']
        print('AI response: ' + ai_output)
        [question, answer] = split_string(ai_output)
        is_valid = check_question_validity(question, answer, type_of_question)

    # Return valid question and answer
    return [question, answer]


def select_random_note_portion(note, max_note_length=200):
    # Truncate note if it's longer than max_note_length
    if len(note) > max_note_length:
        start_idx = random.randint(0, len(note) - max_note_length)
        truncated_note = note[start_idx:start_idx + max_note_length]
    else:
        truncated_note = note
    return truncated_note


def check_question_validity(question: str, answer: str, type_of_question: str) -> bool:
    # Check if the question is a valid true or false question
    if type_of_question == 'true or false':
        if answer.split('.')[0].strip() not in ['TRUE', 'FALSE', 'True', 'False', 'true', 'false']:
            print('Question not valid. Regenerate...')
            return False

    # Check if the question is a valid-closed question
    if type_of_question == 'closed question':
        options = re.findall(r'\b[A-D]\)', question)
        if len(options) < 2:
            print('Question not valid. Regenerate...')
            return False

    # If all checks passed, return True
    print('Valid question!')
    return True


def split_string(input_string: str) -> list:
    try:
        question = re.split(r'QUESTION:\s*', input_string)[1].split('CORRECT ANSWER:')[0]
        answer = re.split(r'CORRECT ANSWER:\s*', input_string)[1]
        return [question, answer]
    except Exception as e:
        print(f"An error occurred while splitting the AI output: {e}")
        return [input_string, ""]
