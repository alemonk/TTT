import openai
import backoff
import random
import re
import logging
import os

logging.basicConfig(level=logging.INFO)

# Set your OpenAI API key
openai_key = os.getenv('api_key')
openai.api_key = openai_key


def log_backoff(details):
    logging.info(f"Backing off {details['wait']} seconds after {details['tries']} tries")


@backoff.on_exception(backoff.expo, openai.error.RateLimitError, max_tries=20, on_backoff=log_backoff, base=10)
def get_openai_response_with_backoff(prompt_question):
    print('request to openai with backoff')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant who has to generate a question."},
                      {"role": "user", "content": prompt_question}
                      ],
            temperature=0.8,
            frequency_penalty=0.3,
            presence_penalty=0.8,
        )
        response = response['choices'][0]['message']['content']
        return response
    except openai.error.RateLimitError as e:
        return 'QUESTION: A LOT of people are using this app, what do you say? ' + \
               'CORRECT ANSWER: True'


def create_random_question(note, type_of_question='true or false', difficulty='medium'):
    # Set up the prompt for openAI API
    truncated_note = select_random_note_portion(note, max_note_length=500)

    prompt_question = "Kind of question: " + type_of_question + \
                      "\nDifficulty: " + difficulty + \
                      "\nAsk one random question using a few sentences from the following:\n" + truncated_note + \
                      "\n\nNote 1: The output must be in the format 'QUESTION: [...] ? CORRECT ANSWER: [...] .' " + \
                      "\nNote 2: In the CORRECT ANSWER, explain also why the answer is correct." + \
                      "\nNote 3: In the case of a 'closed question' there must be A, B, C, or D as possible answers." + \
                      "\nNote 4: In the case of a 'true or false' question, the answer is TRUE/FALSE regardless of the language." + \
                      "\nNote 5: The language MUST be the same as the note, which is not necessarily English." + \
                      "\nNote 6: Give equal chance to the possible answers."

    print('Prompt question: ' + prompt_question)

    # Generate ai response
    ai_output = get_openai_response_with_backoff(prompt_question)
    print(ai_output)

    # Split AI generated output into question and answer
    [question, answer] = split_string(ai_output)

    # Check if generated question is valid
    is_valid = check_question_validity(question, answer, type_of_question)

    # If generated question is not valid, generate a new one
    while not is_valid:
        ai_output = get_openai_response_with_backoff(prompt_question)
        print('AI response: ' + ai_output)
        [question, answer] = split_string(ai_output)
        is_valid = check_question_validity(question, answer, type_of_question)

    # Return valid question and answer
    return [question, answer]


def select_random_note_portion(note, max_note_length):
    # Truncate note if it's longer than max_note_length
    if len(note) > max_note_length:
        start_idx = random.randint(0, len(note) - max_note_length)
        truncated_note = note[start_idx:start_idx + max_note_length]
    else:
        truncated_note = note
    return truncated_note


def check_question_validity(question: str, answer: str, type_of_question: str) -> bool:
    # Check if rpm are too many
    if question == 'A LOT of people are using this app, what do you say? ':
        return True

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
