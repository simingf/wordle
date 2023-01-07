from data import get_wordle_answers, get_wordle_guesses

guesses = get_wordle_answers()
answers = get_wordle_answers()

def filter_answers(guess, result, answers):
    """Return a list of answers that match the given guess and result."""
    return [answer for answer in answers if is_valid(guess, result, answer)]

def is_valid(guess, result, word):
    """Return True if the word matches the given guess and result."""
    # for i in range(5):
    #     if result[i] == 0: # grey => letter not in word
    #         for j in range(5):
    #             if guess[i] == word[j] and result[j] != 2:
    #                 return False
    #     elif result[i] == 1: # yellow => letter in word but not at this position
    #         if guess[i] == word[i] or guess[i] not in word:
    #             return False
    #     elif result[i] == 2: # green => letter in word at this position
    #         if guess[i] != word[i]:
    #             return False
    #     else:
    #         raise ValueError("Invalid result")
    # return True

def next_guess(guesses, answers):
    """Return the next guess for the game."""
    if len(answers) == 1:
        return answers[0]
    best_guess = None
    best_value = 0
    for guess in guesses:
        val = value(guess, answers)
        if val > best_value:
            best_guess = guess
            best_value = val
    return best_guess

def value(guess, answers):
    """Return the value of the given guess."""
    dict = {}
    res = 0
    for answer in answers:
        result = get_result(guess, answer)
        dict[tuple(result)] = dict.get(tuple(result), 0) + 1
    for val in dict.values():
        res += val * (len(answers) - val)
    print("value of", guess, "is", res)
    return res

def get_result(guess, answer):
    """Return the result of the guess for the given answer."""
    res = []
    for i in range(5):
        if guess[i] == answer[i]:
            res += [2]
        elif guess[i] in answer:
            res += [1]
        else:
            res += [0]
    return res

if __name__ == "__main__":
    answers = filter_answers("crane", [0, 1, 0, 0, 1], answers)
    answers = filter_answers("posit", [0, 0, 0, 0, 0], answers)
    answers = filter_answers("bleed", [2, 0, 1, 0, 0], answers)
    print(answers)
    # guess = next_guess(guesses, answers)
    # print(guess)