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
    if len(word) == 1:
        return word

    # randomly delete characters with probability p
    characters = []
    for character in word:
        r = random.uniform(0, 1)
        if r > p:
            characters.append(character)

    new_token = "".join(characters)

    # if you end up deleting all chars, just return a random word
    if len(new_token) == 0:
        rand_int = random.randint(0, len(word) - 1)
        return [word[rand_int]]

    return new_token


########################################################################
# Random swap
# Randomly swap two characters in the token n times
########################################################################

def random_swap(word, n):
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
    word_token = get_only_chars(word_token)
    num_words = len(word_token)

    augmented_tokens = []
    num_new_per_technique = int(num_aug / 4) + 1
    n_rs = max(1, int(alpha_rs * num_words))


    # rs
    for _ in range(num_new_per_technique):
        try:
            a_words = random_swap(word_token, n_rs)
            augmented_tokens.append(''.join(a_words))
        except ValueError:
            print("Cannot handle character")
            pass
    # rd
    for _ in range(num_new_per_technique):
        try:
            a_words = random_deletion(word_token, p_rd)
            augmented_tokens.append(''.join(a_words))
        except ValueError:
            print("Cannot handle character")
            pass
    augmented_tokens = [get_only_chars(word_token) for word_token in augmented_tokens]
    shuffle(augmented_tokens)

    # trim so that we have the desired number of augmented sentences
    if num_aug >= 1:
        augmented_tokens = augmented_tokens[:num_aug]
    else:
        keep_prob = num_aug / len(augmented_tokens)
        augmented_tokens = [s for s in augmented_tokens if random.uniform(0, 1) < keep_prob]

    # append the original sentence
    augmented_tokens.append(word_token)

    return augmented_tokens