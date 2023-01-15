def filter_answers(guess, result, answers):
    """Return a list of answers that match the given guess and result."""
    return [answer for answer in answers if is_valid(guess, result, answer)]

def is_valid(guess, result, word):
    """Return True if the word matches the given guess and result."""
    letters = set({})
    
    for i in range(5):
        letters.add(guess[i])
    
    for letter in letters:
        positions = []
        for i in range(5):
            if guess[i] == letter:
                positions.append(i)

        if len(positions) == 1: # only one letter
            letter_pos = positions[0]
            if result[letter_pos] == 0: # gray
                if letter in word:
                    return False
            elif result[letter_pos] == 1: # yellow
                if guess[letter_pos] == word[letter_pos] or letter not in word:
                    return False
            elif result[letter_pos] == 2: # green
                if guess[letter_pos] != word[letter_pos]:
                    return False

        if len(positions) == 2: # letter appears twice
            pos1 = positions[0]
            pos2 = positions[1]

            # gray gray
            if result[pos1] == 0 and result[pos2] == 0:
                if letter in word:
                    return False

            # yellow gray or gray yellow
            if result[pos1] == 1 and result[pos2] == 0 or result[pos1] == 0 and result[pos2] == 1:
                if count(letter, word) != 1:
                    return False
                elif guess[pos1] == word[pos1]:
                    return False
                elif guess[pos2] == word[pos2]:
                    return False
            
            # green gray
            if result[pos1] == 2 and result[pos2] == 0:
                if count(letter, word) != 1:
                    return False
                elif guess[pos1] != word[pos1]:
                    return False
            
            # gray green 
            if result[pos1] == 0 and result[pos2] == 2:
                if count(letter, word) != 1:
                    return False
                elif guess[pos2] != word[pos2]:
                    return False
                    
            # green yellow
            if result[pos1] == 2 and result[pos2] == 1:
                if count(letter, word) < 2:
                    return False
                elif guess[pos1] != word[pos1]:
                    return False
                elif guess[pos2] == word[pos2]:
                    return False

            # yellow green
            if result[pos1] == 1 and result[pos2] == 2:
                if count(letter, word) < 2:
                    return False
                elif guess[pos1] == word[pos1]:
                    return False
                elif guess[pos2] != word[pos2]:
                    return False

            # green green
            if result[pos1] == 2 and result[pos2] == 2:
                if count(letter, word) != 2:
                    return False
                elif guess[pos1] != word[pos1] or guess[pos2] != word[pos2]:
                    return False
    
        if len(positions) == 3: # letter appears three times
            # I was too lazy to count every case, so I only return false for words which have letters that are gray in the guess
            bad_letters = set({})
            for i in range(5):
                if result[i] == 0:
                    bad_letters.add(guess[i])
            for char in word:
                if char in bad_letters:
                    return False
    
    return True

def count(char, word):
    """Return the number of times char appears in word."""
    return sum([1 for letter in word if letter == char])

def next_guess(guesses, answers):
    """Return the next guess for the game."""
    if len(answers) <= 2:
        return answers[0]
    
    best_guess = None
    best_value = 0

    for guess in guesses:
        val = value(guess, answers)
        # don't care if word is a possible answer as long as it maximizes value
        if val > best_value:
            best_value = val
            best_guess = guess
        # better to guess a word that is in the answers if it also maximizes value
        if val == best_value and guess in answers:
            best_guess = guess
    
    return best_guess

def next_best_guesses(guesses, answers):
    """Return the next best guesses for the game"""
    # only one possible answer left
    if len(answers) == 1:
        return [answers[0]]
    
    # take the 50/50
    if len(answers) == 2:
        return answers

    # find highest possible value
    best_value = 0
    for guess in guesses:
        val = value(guess, answers)
        if val > best_value:
            best_value = val

    # get all possible guesses that maximize value (inclusive / only those in possible answers)
    best_guesses = []
    best_guesses_in_answers = []
    for guess in guesses:
        if value(guess, answers) == best_value:
            best_guesses += [guess]
            if guess in answers:
                best_guesses_in_answers += [guess]

    # better to guess a word that is in the answers if it also maximizes value
    if len(best_guesses_in_answers) > 0:
        return best_guesses_in_answers

    return best_guesses

def value(guess, answers):
    """Return the value of the given guess."""
    dict = {}
    res = 0

    # for a single guess, count the number of times each possible result will occur for the possible answers
    for answer in answers:
        result = get_result(guess, answer)
        dict[tuple(result)] = dict.get(tuple(result), 0) + 1

    # add the probability of getting a result multiplied by the number of potential answers eliminated by that result
    for val in dict.values():
        res += val * (len(answers) - val)

    return res

def get_result(guess, answer):
    """Return the result of the guess for the given answer."""
    # 0 = nothing, 1 = yellow, 2 = green
    output = [0, 0, 0, 0, 0]
    
    # check for correct letter and placement
    for i in range(5):
        if guess[i] == answer[i]:
            output[i] = 2
            answer = answer[:i] + ' ' + answer[i + 1:]
           
    # check for correct letter
    for i in range(5):
        char = guess[i]
        if char in answer and output[i] == 0:
            output[i] = 1
            first_occurence = answer.find(char)
            answer = answer[:first_occurence] + ' ' + answer[first_occurence + 1:]
    return output