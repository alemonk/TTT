import openai
import backoff
import random
import re
from website.static.openai_key import openai_key

# Set your OpenAI API key
openai.api_key = openai_key()


@backoff.on_exception(backoff.expo, openai.error.RateLimitError, max_tries=10)
def get_openai_response_with_backoff(prompt_question):
    print('request to openai with backoff')

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt_question
        }],
        temperature=1
    )
    return response


def create_random_question(note, type_of_question='true or false', difficulty='medium'):
    # Set up the prompt for openAI API
    truncated_note = select_random_note_portion(note, max_note_length=200)

    prompt_question = "Kind of question: " + type_of_question + \
                      "\nDifficulty: " + difficulty + \
                      "\nAsk one random question using a few sentences inside the following:\n" + truncated_note + \
                      "\n\nThe output must be in the format 'QUESTION: [...] ? CORRECT ANSWER: [...] .' " + \
                      "(note: in case of 'closed question' there must be A B C or D as possible answers)"

    response = get_openai_response_with_backoff(prompt_question)
    ai_output = response['choices'][0]['message']['content']
    print('AI response: ' + ai_output)

    # Split AI generated output into question and answer
    [question, answer] = split_string(ai_output)

    return [question, answer]


def select_random_note_portion(note, max_note_length=200):
    # Truncate note if it's longer than max_note_length
    if len(note) > max_note_length:
        start_idx = random.randint(0, len(note) - max_note_length)
        truncated_note = note[start_idx:start_idx + max_note_length]
    else:
        truncated_note = note
    return truncated_note


def split_string(input_string: str) -> list:
    try:
        question = re.split(r'QUESTION:\s*', input_string)[1].split('CORRECT ANSWER:')[0]
        answer = re.split(r'CORRECT ANSWER:\s*', input_string)[1].split('.')[0]
        return [question, answer]
    except Exception as e:
        print(f"An error occurred while splitting the AI output: {e}")
        return [input_string, ""]
