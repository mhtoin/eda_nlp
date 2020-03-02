# Easy data augmentation techniques for text classification
# Jason Wei and Kai Zou

from eda import *
from character_eda import *
import string
import re

# arguments to be parsed from command line
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=str, help="input file of unaugmented data")
ap.add_argument("--output", required=False, type=str, help="output file of unaugmented data")
ap.add_argument("--num_aug", required=False, type=int, help="number of augmented sentences per original sentence")
ap.add_argument("--alpha", required=False, type=float, help="percent of words in each sentence to be changed")
args = ap.parse_args()

# the output file
output = None
if args.output:
    output = args.output
else:
    from os.path import dirname, basename, join

    output = join(dirname(args.input), 'eda_' + basename(args.input))

# number of augmented sentences to generate per original sentence
num_aug = 9  # default
if args.num_aug:
    num_aug = args.num_aug

# how much to change each sentence
alpha = 0.1  # default
if args.alpha:
    alpha = args.alpha


# generate more data with standard augmentation
def gen_eda(train_orig, output_file, alpha, num_aug=9):
    writer = open(output_file, 'w')
    lines = open(train_orig, 'r').readlines()

    for i, line in enumerate(lines):
        parts = line.split('\t')

        # If line actually has two parts, split and augment
        if len(parts) > 1:
            try:
                #print(f"Parts are {parts}")
                label = parts[1]
                token = parts[0]
                #print(f"{token} is {len(token)} long {label}")
                aug_token = edac(token, alpha_rs=alpha, p_rd=alpha, num_aug=num_aug)
                print(aug_token)
                writer.write(aug_token + "\t" + label)
            except TypeError as e:
                print(f"Error with {aug_token} in {line}")
                print(e)
                writer.write(line)
        else:
            #Line is probaly just whitespace, write as is
            print(f"Not handling {line.isspace()}")
            writer.write(line)

    writer.close()
    print("generated augmented sentences with eda for " + train_orig + " to " + output_file + " with num_aug=" + str(
        num_aug))


# main function
if __name__ == "__main__":
    # generate augmented sentences and output into a new file
    gen_eda(args.input, output, alpha=alpha, num_aug=num_aug)
