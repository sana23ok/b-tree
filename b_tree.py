class Node:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.values = []


class BTree:
    def __init__(self, t):
        self.root = Node(True)
        self.t = t
        self.comp = 0

    def search(self, key, node=None):
        node = self.root if node is None else node

        low = 0
        high = len(node.keys) - 1

        while low <= high:
            mid = (low + high) // 2
            guess = node.keys[mid][0]
            self.comp += 1
            if guess == key:
                return node, mid
            elif guess > key:
                high = mid - 1
            else:
                low = mid + 1

        if not node.leaf:
            return self.search(key, node.children[low])

        return None

    @property
    def getNumOfComparisons(self):
        temp = self.comp
        self.comp=0
        return temp

    def devideChild(self, x, i):
        t = self.t

        # y is a full child of x
        y = x.children[i]
        
        # create a new node and add it to x's list of children
        z = Node(y.leaf)
        x.children.insert(i + 1, z)

        # insert the median of the full child y into x
        x.keys.insert(i, y.keys[t - 1])

        # split apart y's keys into y & z
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]

        # if y is not a leaf, we reassign y's children to y & z
        if not y.leaf:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t] # video incorrectly has t-1

    def insert(self, k, v):  # Modify to accept a value v
        t = self.t
        root = self.root

        if len(root.keys) == (2 * t) - 1:
            new_root = Node()
            self.root = new_root
            new_root.children.insert(0, root)
            self.devideChild(new_root, 0)
            self.insertInNotFull(new_root, k, v)  # Pass the value to the insert_non_full function
        else:
            self.insertInNotFull(root, k, v)  # Pass the value to the insert_non_full function

    def insertInNotFull(self, x, k, v):  # Modify to accept a value v
        t = self.t
        i = len(x.keys) - 1

        if x.leaf:
            x.keys.append((None, None))  # Add a placeholder for the new key-value pair
            while i >= 0 and k < x.keys[i][0]:  # Compare the keys
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = (k, v)  # Insert the key-value pair at the correct position
        else:
            while i >= 0 and k < x.keys[i][0]:  # Compare the keys
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * t) - 1:
                self.devideChild(x, i)
                if k > x.keys[i][0]:  # Compare the keys
                    i += 1
            self.insertInNotFull(x.children[i], k, v)

    def delete(self, x, k):
        t = self.t
        i = 0

        while i < len(x.keys) and k > x.keys[i][0]:
            i += 1
        if x.leaf:
            if i < len(x.keys) and x.keys[i][0] == k:
                x.keys.pop(i)
            return

        if i < len(x.keys) and x.keys[i][0] == k:
            return self.deleteInnerNode(x, k, i)
        elif len(x.children[i].keys) >= t:
            self.delete(x.children[i], k)
        else:
            if i != 0 and i + 2 < len(x.children):
                if len(x.children[i - 1].keys) >= t:
                    self.deleteSibling(x, i, i - 1)
                elif len(x.children[i + 1].keys) >= t:
                    self.deleteSibling(x, i, i + 1)
                else:
                    self.deleteMerge(x, i, i + 1)
            elif i == 0:
                if len(x.children[i + 1].keys) >= t:
                    self.deleteSibling(x, i, i + 1)
                else:
                    self.deleteMerge(x, i, i + 1)
            elif i + 1 == len(x.children):
                if len(x.children[i - 1].keys) >= t:
                    self.deleteSibling(x, i, i - 1)
                else:
                    self.deleteMerge(x, i, i - 1)
            self.delete(x.children[i], k)

    def deleteInnerNode(self, x, k, i):
        t = self.t
        if x.leaf:
            if x.keys[i] == k:
                x.keys.pop(i)
            return

        if len(x.children[i].keys) >= t:
            x.keys[i] = self.deletePredecessor(x.children[i])
            return
        elif len(x.children[i + 1].keys) >= t:
            x.keys[i] = self.deleteSuccessor(x.children[i + 1])
            return
        else:
            self.deleteMerge(x, i, i + 1)
            self.deleteInnerNode(x.children[i], k, self.t - 1)

    def deletePredecessor(self, x):
        if x.leaf:
            return x.keys.pop()
        n = len(x.keys) - 1
        if len(x.children[n].keys) >= self.t:
            self.deleteSibling(x, n + 1, n)
        else:
            self.deleteMerge(x, n, n + 1)
        self.deletePredecessor(x.children[n])

    def deleteSuccessor(self, x):
        if x.leaf:
            return x.keys.pop(0)
        if len(x.children[1].keys) >= self.t:
            self.deleteSibling(x, 0, 1)
        else:
            self.deleteMerge(x, 0, 1)
        self.deleteSuccessor(x.children[0])

    def deleteMerge(self, x, i, j):
        cnode = x.children[i]

        if j > i:
            rsnode = x.children[j]
            cnode.keys.append(x.keys[i])
            for k in range(len(rsnode.keys)):
                cnode.keys.append(rsnode.keys[k])
                if len(rsnode.children) > 0:
                    cnode.children.append(rsnode.children[k])
            if len(rsnode.children) > 0:
                cnode.children.append(rsnode.children.pop())
            new = cnode
            x.keys.pop(i)
            x.children.pop(j)
        else:
            lsnode = x.children[j]
            lsnode.keys.append(x.keys[j])
            for i in range(len(cnode.keys)):
                lsnode.keys.append(cnode.keys[i])
                if len(lsnode.children) > 0:
                    lsnode.children.append(cnode.children[i])
            if len(lsnode.children) > 0:
                lsnode.children.append(cnode.children.pop())
            new = lsnode
            x.keys.pop(j)
            x.children.pop(i)

        if x == self.root and len(x.keys) == 0:
            self.root = new

    @staticmethod
    def deleteSibling(x, i, j):
        cnode = x.children[i]
        if i < j:
            rsnode = x.children[j]
            cnode.keys.append(x.keys[i])
            x.keys[i] = rsnode.keys[0]
            if len(rsnode.children) > 0:
                cnode.children.append(rsnode.children[0])
                rsnode.children.pop(0)
            rsnode.keys.pop(0)
        else:
            lsnode = x.children[j]
            cnode.keys.insert(0, x.keys[i - 1])
            x.keys[i - 1] = lsnode.keys.pop()
            if len(lsnode.children) > 0:
                cnode.children.insert(0, lsnode.children.pop())

    def update(self, key, new_value):
        node, index = self.search(key)
        if node is None:
            return False
        else:
            node.keys[index] = (key, new_value)
            return True

    def print_tree(self, x, level=0):
        print(f'Level {level}', end=": ")

        for i in x.keys:
            print(i, end=" ")

        print()
        level += 1

        if len(x.children) > 0:
            for i in x.children:
                self.print_tree(i, level)

    def print_btree(self, node, l=0):
        print(' ' * l, node.keys)
        l += 1
        if len(node.child) > 0:
            for child in node.child:
                self.print_btree(child, l)


