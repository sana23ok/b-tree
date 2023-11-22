# B-Tree Implementation with PyQt5 UI

## Introduction

This project combines a B-tree data structure with a PyQt5-based user interface for interactive operations on the tree. The B-tree implementation is designed to handle efficient insertion, deletion, search, and modification of keys.

## Project Structure

The project is organized into the following components:

1. **User Interface (UI):**
   - The PyQt5-based UI is implemented in the `MainWindow` class located in the `pyUI` module.
   - The UI provides buttons for operations such as Insert, Delete, Search, Modify, Generate DB, Read DB, and Drop DB.
   - A QTableWidget displays the current state of the B-tree, and a QLineEdit allows users to input keys for various operations.

2. **B-Tree Implementation:**
   - The B-tree logic is implemented in the `BTree` class within the `build_tree` module.
   - Nodes in the B-tree are represented by the `Node` class.
   - The B-tree supports search operations with a specified key and maintains a count of the number of comparisons made during the search.

3. **Data Generation:**
   - The project includes a `generation` module responsible for generating a sample database (db.txt) with specified parameters.

## Getting Started

### Prerequisites

- Python 3.11.2
- PyQt5 5.15.2

### Installation

1. Clone the repository
2. Install dependencies
3. Run the application:
    ```bash
    python main.py
    ```

## UI Usage

- **Insert:** Insert a key into the B-tree.
- **Delete:** Delete a key from the B-tree.
- **Search:** Search for a key in the B-tree.
- **Modify:** Modify a key in the B-tree.
- **Generate DB:** Generate a sample database with specified parameters.
- **Read DB:** Read the generated database.
- **Drop DB:** Drop the current database.
