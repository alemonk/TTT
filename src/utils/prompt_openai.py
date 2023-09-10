def prompt_openai(language, type_of_question):

    if language == 'it':
        openai_prompt = "Sei un assistente utile che deve generare una domanda. " + \
                        'Ti verrà fornita una porzione casuale di un testo o libro percui, quando generi una domanda, evita riferimenti alle sue figure ' + \
                        "ai suoi capitoli, alle sue righe o pagine come se l'utente fosse a conoscenza del libro a memoria (vedi Commento 5). " + \
                        'La domanda dovrebbe essere più focalizzata sulla comprensione della porzione piuttosto che sulla sua grammatica. ' + \
                        'Tipo di domanda: ' + type_of_question + '.' + \
                        "\nCommento 1: L'output deve essere nel formato 'QUESTION: [domanda] ? CORRECT ANSWER: [risposta] .' " + \
                        "\nCommento 2: Nella CORRECT ANSWER, spiega anche perché la risposta è corretta." + \
                        "\nCommento 3: Nel caso di 'closed question', ci devono essere A, B, C o D come possibili soluzioni." + \
                        "\nCommento 4: Nel caso di 'true or false', la risposta può essere TRUE o FALSE."

    else:
        openai_prompt = "You are a helpful assistant who has to generate a question. " + \
                        'You are given a random portion of a text or book so, when you generate a question, avoid referring to its figures, ' + \
                        'to its chapters, its lines or pages as if the user knew all the book by heart (see Remark 5). ' + \
                        'The question should be more focused on the understanding of the portion rather than its grammar. ' + \
                        'Kind of question: ' + type_of_question + '.' + \
                        "\nRemark 1: The output must be in the format 'QUESTION: [question] ? CORRECT ANSWER: [answer] .' " + \
                        "\nRemark 2: In the CORRECT ANSWER, explain also why the answer is correct." + \
                        "\nRemark 3: In the case of a 'closed question' there must be A, B, C, or D as possible answers." + \
                        "\nRemark 4: In the case of a 'true or false' question, the answer is either TRUE or FALSE."

    return openai_prompt
