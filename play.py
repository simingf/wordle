from data import get_wordle_answers, get_wordle_guesses
from solve import filter_answers, next_guess

guesses = get_wordle_answers()
answers = get_wordle_answers()

if __name__ == "__main__":
    guess = str(input("what is your initial guess?\n"))
    print()
    for i in range(6):
        print("Turn", i + 1)
        print(guess)
        result = str(input("result:\n"))
        result = [int(x) for x in result]
        answers = filter_answers(guess, result, answers)
        if len(answers) == 1:
            print("The answer is", answers[0])
            break
        guess = next_guess(guesses, answers)
        print()
 