def get_wordle_guesses():
    words = []
    with open("wordle_guesses.txt", "r") as f:
        for line in f:
            words.append(line.strip())
    return words

def get_wordle_answers():
    words = []
    with open("wordle_answers.txt", "r") as f:
        for line in f:
            words.append(line.strip())
    return words