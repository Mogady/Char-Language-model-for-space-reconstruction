#!/usr/bin/env python3

### usage python test_spaces.py <predicted file> <test file>
from __future__ import print_function

import sys
import re
import argparse

parser = argparse.ArgumentParser(description='Compare spaces in reference file and test file.')
parser.add_argument('reference_file', action="store")
parser.add_argument('test_file', action="store")
args = parser.parse_args()

file1 = open(args.reference_file, encoding="utf-8")
file2 = open(args.test_file, encoding="utf-8")

true_positive = 0
false_negative = 0
false_positive = 0

for line1, line2 in zip(file1, file2):
    line1 = line1.rstrip('\n')
    line2 = line2.rstrip('\n')
    if re.sub(' ', '', line1) != re.sub(' ', '', line2):
        print("Files shouldn't have any differences other than spaces:", file=sys.stderr)
        print(line1, file=sys.stderr)
        print(line2, file=sys.stderr)
        sys.exit(12)

    i1 = 0
    i2 = 0
    while i1<len(line1) and i2<len(line2):
        is_first_space = (line1[i1] == ' ')
        is_second_space = (line2[i2] == ' ')
        if is_first_space and is_second_space:
            true_positive += 1
            i1 += 1
            i2 += 1
        elif is_first_space:
            false_negative += 1
            i1+=1
        elif is_second_space:
            false_positive += 1
            i2+=1
        else:
            i1 += 1
            i2 += 1

if file1.readline() or file2.readline():
    print("Files should have equal number of lines", file=sys.stderr)
    sys.exit(13)

p = float(true_positive) / (true_positive + false_positive) if (true_positive + false_positive)>0 else 0.0
r = float(true_positive) / (true_positive + false_negative) if (true_positive + false_negative)>0 else 0.0
f1 = 2*p*r / (p+r) if p+r>0 else 0.0
print("Precision: ", p)
print("Recall: ", r)
print("F1: ", f1)
