def prompt_check_answer_user(language, question, answer, guess):
    if language == 'it':
        user_prompt = f"""
                    Domanda: {question}
                    Risposta corretta: {answer}
                    Tentativo dell'utente: {guess}
                    Convalida: è il tentativo di risposta "{guess}" una risposta valida per la domanda "{question}" basata sulla risposta corretta "{answer}"?
                    Nota 1: Se il tentativo non è valido, rispondi con una possibile risposta corretta di circa 200 parole.
                    Nota 2: Valuta in modo verbale il tentativo di risposta fornito (ad esempio, evidenzia se risulta eccessivamente breve or repetitive).
                    """

    else:
        user_prompt = f"""
                    Question: {question}
                    Correct Answer: {answer}
                    User guess: {guess}
                    Validation: Is the guess "{guess}" a valid answer for the question "{question}" based on the correct answer "{answer}"?
                    Remark 1: If it is not valid, answer with a possible correct answer of about 200 words.
                    Remark 2: Verbally evaluate the provided answer attempt (for example, highlight if it is too short or repetitive). 
                    """

    return user_prompt
