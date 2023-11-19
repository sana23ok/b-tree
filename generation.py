import numpy as np


def generateDB(n, filename, start, end):
    # Generate a random array of integers
    random_array = np.random.randint(start, end, n)

    # Write the array to a file
    with open(filename, 'w') as f:
        for item in random_array:
            f.write(str(item)+"\n")

        f.close()
