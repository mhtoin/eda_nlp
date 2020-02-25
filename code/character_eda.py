# Easy data augmentation techniques for word classification
# Miika Oinonen
# Adapted from eda by Jason Wei and Kai Zou

import random
from random import shuffle
import string

random.seed(1)

# stop words list
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our',
              'ours', 'ourselves', 'you', 'your', 'yours',
              'yourself', 'yourselves', 'he', 'him', 'his',
              'himself', 'she', 'her', 'hers', 'herself',
              'it', 'its', 'itself', 'they', 'them', 'their',
              'theirs', 'themselves', 'what', 'which', 'who',
              'whom', 'this', 'that', 'these', 'those', 'am',
              'is', 'are', 'was', 'were', 'be', 'been', 'being',
              'have', 'has', 'had', 'having', 'do', 'does', 'did',
              'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
              'because', 'as', 'until', 'while', 'of', 'at',
              'by', 'for', 'with', 'about', 'against', 'between',
              'into', 'through', 'during', 'before', 'after',
              'above', 'below', 'to', 'from', 'up', 'down', 'in',
              'out', 'on', 'off', 'over', 'under', 'again',
              'further', 'then', 'once', 'here', 'there', 'when',
              'where', 'why', 'how', 'all', 'any', 'both', 'each',
              'few', 'more', 'most', 'other', 'some', 'such', 'no',
              'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
              'very', 's', 't', 'can', 'will', 'just', 'don',
              'should', 'now', '']

# cleaning up text - not sure if this is needed or if
# some other sort of cleaning up is needed
import re


def get_only_chars(line):
    clean_line = ""

    line = line.replace("’", "")
    line = line.replace("'", "")
    line = line.replace("-", " ")  # replace hyphens with spaces
    line = line.replace("\t", " ")
    line = line.replace("\n", " ")
    #line = line.lower()

    for char in line:
        if char in 'qwertyuiopasdfghjklzxcvbnmåäöQWERTYUIOPÅASDFGHJKLÖÄZXCVBNM ':
            clean_line += char
        else:
            clean_line += ' '

    clean_line = re.sub(' +', ' ', clean_line)  # delete extra spaces
    if clean_line[0] == ' ':
        clean_line = clean_line[1:]
    return clean_line


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
