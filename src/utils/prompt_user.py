def prompt_user(language, truncated_note):
    if language == 'it':
        user_prompt = "Fammi una domanda random usando alcune frasi dal seguente: " + truncated_note

    else:
        user_prompt = "Ask one random question using a few sentences from the following: " + truncated_note

    return user_prompt
