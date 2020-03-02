# Easy data augmentation techniques for word classification
# Miika Oinonen
# Adapted from eda by Jason Wei and Kai Zou

import random
from random import shuffle
import string

random.seed(1)


########################################################################
# Random deletion
# Randomly delete characters from the token with probability p
########################################################################

def random_deletion(word, p):
    # don't delete tokens of just one character
    print(f"Word is {word} and it's {len(word)} long")
    if len(word) < 2:
        return word

    # randomly delete characters with probability p
    characters = []
    new_token = ""
    for character in word:
        r = random.uniform(0, 1)
        print(f"Starting deletion, r is {r} and p is {p}")
        if r > p:
            new_token += character
            print(f"Token is {new_token} at the moment")
            #characters.append(character)

    #new_token = "".join(characters)

    # if you end up deleting all chars, just return a random word
    if len(new_token) == 0:
        print("Empty token!")
        rand_int = random.randint(0, len(word) - 1)
        random_word = word[rand_int]
        print(f"Empty token, returning {random_word} instead")
        return random_word

    return new_token


########################################################################
# Random swap
# Randomly swap two characters in the token n times
########################################################################

def random_swap(word, n):
    # Makes no sense to try to swap something with only 1 token
    if len(word) < 2:
        return word
    characters = [char for char in word]
    new_word = ""
    for _ in range(n):
        new_word = swap_chars(characters)
    return new_word


def swap_chars(characters):
    random_idx_1 = random.randint(0, len(characters) - 1)
    random_idx_2 = random_idx_1
    counter = 0
    while random_idx_2 == random_idx_1:
        random_idx_2 = random.randint(0, len(characters) - 1)
        counter += 1
        if counter > 3:
            return "".join(characters)
    characters[random_idx_1], characters[random_idx_2] = characters[random_idx_2], characters[random_idx_1]
    return "".join(characters)

def edac(word_token, alpha_rs=0.1, p_rd=0.1, num_aug=9):
    # Cleans the line/token - check if needed?
    #word_token = get_only_chars(word_token)
    num_words = len(word_token)

    n_rs = max(1, int(alpha_rs * num_words))
    choices = [1, 2, 3]

    # For each token choose to either swap, delete or just return the word
    technique = random.choice(choices)

    if technique == 1:
        print("Swapping")
        return random_swap(word_token, n_rs)
    elif technique == 2:
        print("Deleting")
        return random_deletion(word_token, n_rs)
    else:
        print("Doing nothing")
        return word_token
