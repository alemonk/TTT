import backoff
import openai
from website.static.openai_key import openai_key

# Set your OpenAI API key
openai.api_key = openai_key()


@backoff.on_exception(backoff.expo, openai.error.RateLimitError, max_tries=10)
def get_openai_response_with_backoff(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt
        }],
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
