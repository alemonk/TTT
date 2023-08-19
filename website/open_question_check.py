import openai
from website.static.openai_key import openai_key


def open_question_check(guess, question, answer):
    # Set your OpenAI API key
    openai.api_key = openai_key()

    # Construct the prompt
    prompt = f"""
    Question: {question}

    Correct Answer: {answer}

    Guess: {guess}

    Validation: Is the guess "{guess}" a valid answer for the question "{question}" based on the correct answer "{answer}"? If it is not valid, respond with a possible correct answer."
    """

    # Generate AI response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=0.7
    )
    ai_output = response['choices'][0]['message']['content'].strip()

    return ai_output
