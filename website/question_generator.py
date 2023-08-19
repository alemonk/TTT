import time

import openai
import random
from website.static.openai_key import openai_key


def question_generator(note, type_of_question='true or false', difficulty='medium'):
    # Set your OpenAI API key
    openai.api_key = openai_key()

    # Set up the prompt for openAI API
    max_note_length = 800  # Define the maximum length
    if len(note) > max_note_length:
        start_idx = random.randint(0, len(note) - max_note_length)
        truncated_note = note[start_idx:start_idx + max_note_length]
    else:
        truncated_note = note

    prompt_question = "Kind of question: " + type_of_question + \
                      "\nDifficulty: " + difficulty + \
                      "\nAsk one random question using a few sentences inside the following:\n" + truncated_note + \
                      "\n\nThe output must be in the format 'QUESTION: [...] ? CORRECT ANSWER: [...] .' " + \
                      "(note: in case of 'closed question' there must be A B C or D as possible answers)"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt_question
            }],
            temperature=1
        )

        ai_output = response['choices'][0]['message']['content']
        print('AI response: ' + ai_output)

        # Split AI generated output into question and answer
        [question, answer] = split_string(ai_output)

        return [question, answer]
    except Exception as e:
        print("Error " + str(e) + " occurred while generating the question. Retrying in 5 seconds...")
        time.sleep(20)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt_question
            }],
            temperature=1
        )

        ai_output = response['choices'][0]['message']['content']
        print('AI response: ' + ai_output)

        # Split AI generated output into question and answer
        [question, answer] = split_string(ai_output)

        return [question, answer]


def split_string(input_string: str) -> list:
    try:
        question = input_string.split('QUESTION: ')[1].split('CORRECT ANSWER:')[0]
        answer = input_string.split('CORRECT ANSWER: ')[1].split('.')[0]
        return [question, answer]
    except Exception as e:
        print(f"An error occurred while splitting the AI output: {e}")
        return [input_string, ""]
