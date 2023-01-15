from data import get_wordle_guesses, get_wordle_answers
from solve import filter_answers, next_best_guesses, value

valid_user_guesses = get_wordle_guesses() # all valid guesses user can make
program_guesses = get_wordle_answers() # guesses the program can recommend, otherwise program takes too long to run
answers = get_wordle_answers() # will be filtered so can't use same list as program_guesses

def valid_result(result):
    if len(result) != 5:
        return False
    for i in range(5):
        if result[i] != '0' and result[i] != '1' and result[i] != '2':
            return False
    return True

if __name__ == "__main__":
    guess = str(input("What is your initial guess?\n"))
    while guess not in valid_user_guesses:
        print("Invalid Guess, Try Again")
        guess = str(input("What is your initial guess?\n"))
    print()
    for i in range(6):
        print("Turn", i + 1)
        print("Guess: \"" + guess + "\"")
        result = str(input("Result: "))
        while not valid_result(result):
            print("Invalid Result, Try Again")
            result = str(input("Result: "))
        result = [int(x) for x in result]
        answers = filter_answers(guess, result, answers)
        if len(answers) == 1:
            print("The answer is \"" + answers[0] + "\"")
            break
        best_guesses = next_best_guesses(program_guesses, answers)
        val = round(value(best_guesses[0], answers) / len(answers), 2)
        print("Number of possible answers left:", len(answers))
        if len(answers) <= 10:
            print("The possible answers are", answers)
        if len(best_guesses) == 1:
            print("The best guess is \"" + best_guesses[0] + "\"")
            print("This guess is expected to eliminate", val, "possible answers")
        else:
            print("The best guesses are", best_guesses)
            print("These guesses are expected to eliminate", val, "possible answers")
        guess = str(input("Next guess: "))
        while guess not in valid_user_guesses:
            print("Invalid Guess, Try Again")
            guess = str(input("Next guess: "))
        print()
 