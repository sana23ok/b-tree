from b_tree import BTree


def build_Btree(t, filename):
    with open(filename, 'r') as file:
        # Read all lines into a list
        lines = file.readlines()

    if lines:
        B = BTree(t)
        for line in lines:
            number, string = line.strip().split(' ')
            B.insert(int(number), string)
        B.print_tree(B.root)
        return B
    else:
        print(f"{filename} is empty!")
        return None

