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
            return True
    
    return True

def count(char, word):
    """Return the number of times char appears in word."""
    return sum([1 for letter in word if letter == char])

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