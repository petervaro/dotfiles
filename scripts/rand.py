#!/usr/bin/env python3
## INFO ##
## INFO ##

# Import python modules
from sys    import argv
from random import random, shuffle

# Try to get the first argument
try:
    length = int(argv[1])
except IndexError:
    length = 12

# Report to user
print('Generate random number with a length:', length)

# Get proper length number
number = ''
while len(number) < length:
    number += str(random())[2:]

# Shuffle the characters
number = list(number)
shuffle(number)

# Return the random number
print(''.join(number[:length]))
