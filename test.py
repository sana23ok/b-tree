import os
import unittest
from b_tree import BTree
from build_tree import build_Btree
from generation import generateDB


class MyTestCase(unittest.TestCase):
    def test_generateDB(self):
        # Define test parameters
        n = 5
        filename = "test_db.txt"
        start = 100
        end = 200

        # Run the function
        generateDB(n, filename, start, end)

        # Check if the file is created
        self.assertTrue(os.path.isfile(filename))

        # Check if the file contains the correct number of lines
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), n)

        # Check if each line has the correct format
        for line in lines:
            parts = line.strip().split()
            self.assertEqual(len(parts), 2)
            num, str_ = parts
            self.assertTrue(num.isdigit())
            self.assertEqual(len(str_), 10)

        # Clean up: Delete the test file
        os.remove(filename)

    def setUp(self):
        # Create a BTree with a specific order (t)
        self.btree = BTree(t=3)  # Adjust the order 't' as needed
        # Create a temporary file for testing
        self.filename = 'test_input.txt'
        with open(self.filename, 'w') as file:
            file.write("10 A\n20 B\n5 C\n6 D\n12 E\n30 F\n7 G\n17 H\n")

    def test_insert_and_search(self):
        keys = [10, 20, 5, 6, 12, 30, 7, 17]

        # Insert keys into the B-tree
        for key in keys:
            self.btree.insert(key, " " + str(key))

        # Search for each key and verify the correctness of the search
        for key in keys:
            result = self.btree.search(key)
            self.assertIsNotNone(result, f"Key {key} not found in B-tree")
            node, index = result
            self.assertEqual(node.keys[index][0], key, "Incorrect key found in B-tree")

    def test_nonexistent_key(self):
        # Search for a key that doesn't exist in the B-tree
        result = self.btree.search(100)
        self.assertIsNone(result, "Nonexistent key found in B-tree")

    def test_search_empty_tree(self):
        # Search in an empty B-tree
        empty_btree = BTree(t=3)  # Create an empty B-tree
        result = empty_btree.search(5)
        self.assertIsNone(result, "Search in an empty B-tree should return None")

    def test_insert_and_search_with_values(self):
        keys_and_values = [(10, 'A'), (20, 'B'), (5, 'C'), (6, 'D'), (12, 'E'), (30, 'F'), (7, 'G'), (17, 'H')]

        for key, value in keys_and_values:
            self.btree.insert(key, value)

        for key, value in keys_and_values:
            result = self.btree.search(key)
            self.assertIsNotNone(result, f"Key {key} not found in B-tree")
            node, index = result
            self.assertEqual(node.keys[index][0], key, "Incorrect key found in B-tree")
            self.assertEqual(node.keys[index][1], value, "Incorrect value found in B-tree")

    def test_insert_duplicate_key(self):
        keys_and_values = [(10, 'A'), (20, 'B'), (10, 'C')]

        for key, value in keys_and_values:
            self.btree.insert(key, value)

        result = self.btree.search(10)
        self.assertIsNotNone(result, "Duplicate key not found in B-tree")
        node, index = result
        self.assertEqual(node.keys[index][0], 10, "Incorrect key found in B-tree")
        self.assertEqual(node.keys[index][1], 'C', "Incorrect value found in B-tree")

    def test_insert_in_empty_tree(self):
        self.btree.insert(15, 'X')
        result = self.btree.search(15)
        self.assertIsNotNone(result, "Key not found in B-tree")
        node, index = result
        self.assertEqual(node.keys[index][0], 15, "Incorrect key found in B-tree")
        self.assertEqual(node.keys[index][1], 'X', "Incorrect value found in B-tree")

    def test_insert_and_delete(self):
        keys_and_values = [(10, 'A'), (20, 'B'), (5, 'C'), (6, 'D'), (12, 'E'), (30, 'F'), (7, 'G'), (17, 'H')]

        # Insert keys and values into the B-tree
        for key, value in keys_and_values:
            self.btree.insert(key, value)

        # Delete some keys from the B-tree
        keys_to_delete = [10, 30, 5]
        for key in keys_to_delete:
            self.btree.delete(self.btree.root, key)

        # Verify that the deleted keys are no longer present in the B-tree
        for key in keys_to_delete:
            result = self.btree.search(key)
            self.assertIsNone(result, f"Deleted key {key} found in B-tree")

    def test_delete_nonexistent_key(self):
        # Try to delete a key that doesn't exist in the B-tree
        self.btree.insert(10, 'A')
        self.btree.insert(20, 'B')
        self.btree.delete(self.btree.root, 30)  # Deleting a key that doesn't exist
        result = self.btree.search(20)
        self.assertIsNotNone(result, "Key 20 not found in B-tree")
        node, index = result
        self.assertEqual(node.keys[index][0], 20, "Incorrect key found in B-tree")

    def test_delete_and_search_with_values(self):
        keys_and_values = [(10, 'A'), (20, 'B'), (5, 'C'), (6, 'D'), (12, 'E'), (30, 'F'), (7, 'G'), (17, 'H')]

        # Insert keys and values into the B-tree
        for key, value in keys_and_values:
            self.btree.insert(key, value)

        # Delete and search for keys, verifying values
        keys_to_delete = [10, 30, 5]
        for key in keys_to_delete:
            result = self.btree.search(key)
            self.assertIsNotNone(result, f"Key {key} not found in B-tree before deletion")
            node, index = result
            self.assertEqual(node.keys[index][0], key, "Incorrect key found in B-tree before deletion")
            self.btree.delete(self.btree.root, key)
            result = self.btree.search(key)
            self.assertIsNone(result, f"Deleted key {key} found in B-tree")

    def test_delete_duplicate_key(self):
        # Delete a key with duplicates and ensure the correct value is retained
        self.btree.insert(10, 'A')
        self.btree.insert(20, 'B')
        self.btree.insert(10, 'C')  # Duplicate key
        self.btree.delete(self.btree.root, 10)
        result = self.btree.search(10)
        self.assertIsNotNone(result, "Key 10 not found in B-tree")
        node, index = result
        self.assertEqual(node.keys[index][0], 10, "Incorrect key found in B-tree after deletion")
        self.assertEqual(node.keys[index][1], 'C', "Incorrect value found in B-tree after deletion")

    def tearDown(self):
        # Remove the temporary file after testing
        os.remove(self.filename)

    def test_build_Btree(self):
        t = 3  # Adjust the order 't' as needed
        B = build_Btree(t, self.filename)

        # Check if B is an instance of BTree
        self.assertIsInstance(B, BTree, "build_Btree did not return an instance of BTree")

        # Check if the B-tree is built correctly
        keys_and_values = [(10, 'A'), (20, 'B'), (5, 'C'), (6, 'D'), (12, 'E'), (30, 'F'), (7, 'G'), (17, 'H')]
        for key, value in keys_and_values:
            result = B.search(key)
            self.assertIsNotNone(result, f"Key {key} not found in B-tree")
            node, index = result
            self.assertEqual(node.keys[index][0], key, "Incorrect key found in B-tree")
            self.assertEqual(node.keys[index][1], value, "Incorrect value found in B-tree")

    def test_empty_file(self):
        # Test with an empty file
        empty_filename = 'empty_test_input.txt'
        with open(empty_filename, 'w') as f:
            pass  # Create an empty file

        B = build_Btree(3, empty_filename)

        self.assertIsNone(B, "build_Btree did not return None for an empty file")


if __name__ == '__main__':
    unittest.main()
