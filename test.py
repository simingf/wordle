from data import get_wordle_answers, get_wordle_guesses

from solve import filter_answers, next_guess, get_result
import random

all_words = get_wordle_answers()

def test(answer):
    guess = "arise"
    guesses = all_words
    answers = all_words

    if answer == "arise":
        return 1
    
    for j in range(5):
        result = get_result(guess, answer)
        answers = filter_answers(guess, result, answers)
        if len(answers) == 1:
            return j + 2
        guess = next_guess(guesses, answers)
    
    print("Failed")
    return 0

if __name__ == "__main__":
    trials = 100
    total_turns_taken = 0
    success = 0
    for i in range(trials):
        answer = random.choice(all_words)
        turns = test(answer)
        total_turns_taken += turns
        if turns != 0:
            success += 1
        print("Game", i, ", ", answer, ": ", turns, "turns", flush=True)
    print("Success rate:", success / trials)
    print("Average turns taken:", total_turns_taken / success)