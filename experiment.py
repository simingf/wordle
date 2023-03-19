from data import get_wordle_answers, get_wordle_guesses

def count(char, word):
    """Return the number of times char appears in word."""
    return sum([1 for letter in word if letter == char])

guesses = get_wordle_guesses()
answers = get_wordle_answers()
print(len(guesses))
print(len(answers))

words = []

for answer in answers:
    letters = set({})
    for char in answer:
        letters.add(char)
    for char in letters:
        cnt = count(char,answer)
        if cnt == 3:
            words += [answer]
            print(answer)
            continue

print(len(words))
