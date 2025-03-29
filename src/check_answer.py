import backoff
from openai import OpenAI
from .openai_key import openai_key

client = OpenAI(api_key=openai_key)
from openai import RateLimitError
import logging
import os
from .utils.prompt_check_answer_user import prompt_check_answer_user
from .utils.prompt_check_answer_openai import prompt_check_answer_openai
from .models import User
from flask_login import current_user

logging.basicConfig(level=logging.INFO)

# Set your OpenAI API key
openai_key = os.getenv('api_key')


def log_backoff(details):
    logging.info(f"Backing off {details['wait']} seconds after {details['tries']} tries")


@backoff.on_exception(
    backoff.expo,  # Exponential backoff
    RateLimitError,  # Use openai.RateLimitError instead of openai.error.RateLimitError
    max_tries=10,
    on_backoff=log_backoff,
    base=10
)
def get_openai_response_with_backoff(user_prompt, system_prompt):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.5)
    return response


def check_answer(guess, question, answer):
    # Get preferred language
    user = User.query.get(current_user.id)
    language = user.language

    # Construct the prompt
    user_prompt = prompt_check_answer_user(language, question, answer, guess)
    system_prompt = prompt_check_answer_openai(language)

    # Generate AI response
    response = get_openai_response_with_backoff(user_prompt, system_prompt)
    ai_output = response.choices[0].message.content.strip()
    print('\n\nAI response: ' + ai_output)
    return ai_output
