import openai
import random


def question_generator(note, type_of_question='true or false', difficulty='medium'):
    # Set your OpenAI API key
    openai.api_key = "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"

    # Set up the prompt for openAI API
    max_note_length = 500  # Define the maximum length
    if len(note) > max_note_length:
        start_idx = random.randint(0, len(note) - max_note_length)
        truncated_note = note[start_idx:start_idx + max_note_length]
    else:
        truncated_note = note

    prompt_question = "Kind of question: " + type_of_question + \
                      ". Difficulty: " + difficulty + \
                      ". Ask one random question based on the following topic: \n" + truncated_note + \
                      ". The output must be in the format 'QUESTION: ... ? CORRECT ANSWER: ... .'"

    # Generate question
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{
            "role": "user",
            "content": prompt_question
        }],
        temperature=1
    )
    ai_output = response['choices'][0]['message']['content']

    # Split AI generated output into question and answer
    [question, answer] = split_string(ai_output)

    return [question, answer]


def split_string(input_string: str) -> list:
    question = input_string.split('QUESTION: ')[1].split('CORRECT ANSWER:')[0]
    answer = input_string.split('CORRECT ANSWER: ')[1].split('.')[0]
    return [question, answer]
