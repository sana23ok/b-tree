from b_tree import BTree


def build_Btree(t, filename):

    with open(filename, 'r') as file:
        # Read all lines into a list
        lines = file.readlines()

    if lines:
        B = BTree(t)
        for i in range(len(lines)):
            B.insert(int(lines[i]))
        return B
    else:
        print(f"{filename} is empty!")
        return None
