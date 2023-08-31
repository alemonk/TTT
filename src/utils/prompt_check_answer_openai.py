def prompt_check_answer_openai(language):
    if language == 'it':
        system_prompt = 'Tu sei un insegnante che deve correggere la risposta di uno studente'

    else:
        system_prompt = "You are a teacher who has to correct a student's answer."

    return system_prompt
