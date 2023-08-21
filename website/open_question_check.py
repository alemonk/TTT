import backoff
import openai
import logging
import os

logging.basicConfig(level=logging.INFO)

# Set your OpenAI API key
openai_key = os.getenv('api_key')
openai.api_key = openai_key


def log_backoff(details):
    logging.info(f"Backing off {details['wait']} seconds after {details['tries']} tries")


@backoff.on_exception(backoff.expo, openai.error.RateLimitError, max_tries=10, on_backoff=log_backoff, base=5)
def get_openai_response_with_backoff(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a teaching assistant who has to correct an answer."},
                  {"role": "user", "content": prompt}
                  ],
        temperature=0.5
    )
    return response


def open_question_check(guess, question, answer):
    # Construct the prompt
    prompt = f"""
    Question: {question}

    Correct Answer: {answer}

    Guess: {guess}

    Validation: Is the guess "{guess}" a valid answer for the question "{question}" based on the correct answer "{answer}"? If it is not valid, respond with a possible correct answer."
    """

    # Generate AI response
    response = get_openai_response_with_backoff(prompt)
    ai_output = response['choices'][0]['message']['content'].strip()
    print('AI response: ' + ai_output)
    return ai_output
