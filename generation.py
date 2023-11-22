import numpy as np
import random
import string


def generateDB(n, filename, start, end):
    random_array = np.random.randint(start, end, n)

    random_strings = [''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) for _ in range(n)]

    # Write the arrays to a file
    with open(filename, 'w') as f:
        for num, str_ in zip(random_array, random_strings):
            f.write(str(num) + " " + str_ + "\n")

    f.close()
