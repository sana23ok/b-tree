import os
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QPushButton, QHBoxLayout, QLineEdit, QLabel, QLCDNumber, QMessageBox, QInputDialog
from setStyles import style_buttons, style_table, style_lcd_number, style_value_input, style_label
from generation import generateDB
from build_tree import build_Btree


class MainWindow(QMainWindow):
    def __init__(self, n, t, file='db.txt', parent=None):
        super(MainWindow, self).__init__(parent)
        self.widget = QWidget(self)
        self.layout = QHBoxLayout(self.widget)
        # self.resize(600, self.sizeHint().height())
        self.my_file = file
        self.t=t
        generateDB(n, self.my_file, 1, 100000)
        self.B = build_Btree(self.t, self.my_file)

        # self.B.print_tree(self.B.root)
        self.layout.setContentsMargins(40, 20, 20, 20)

        # Left side layout (labels, buttons, and text field)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 10, 80, 10)
        # Add labels
        label_value = QLabel("Key:", self)
        left_layout.addWidget(label_value)

        # Add a QLineEdit for entering values
        self.value_input = QLineEdit(self)
        self.value_input.setPlaceholderText("Enter a key...")
        style_value_input(self)
        left_layout.addWidget(self.value_input)

        # Add buttons
        self.button_insert = QPushButton('Insert', self)
        self.button_insert.clicked.connect(self.conductInsertion)

        self.button_delete = QPushButton('Delete', self)
        self.button_delete.clicked.connect(self.conductDeletion)

        self.button_search = QPushButton('Search', self)
        self.button_search.clicked.connect(self.conductSearch)

        self.button_modify = QPushButton('Modify', self)
        self.button_modify.clicked.connect(self.conductModification)

        # Add left layout to main layout
        self.layout.addLayout(left_layout)

        # Add buttons to layout
        left_layout.addWidget(self.button_insert)
        left_layout.addWidget(self.button_delete)
        left_layout.addWidget(self.button_search)
        left_layout.addWidget(self.button_modify)

        # Add a stretch to separate buttons from the table
        left_layout.addStretch(1)

        # Add left layout to main layout
        self.layout.addLayout(left_layout)

        label_value = QLabel(f"Comparisons:", self)
        left_layout.addWidget(label_value)
        self.lcd_number = QLCDNumber(self)
        left_layout.addWidget(self.lcd_number)

        style_lcd_number(self)

        # Add a margin below buttons
        left_layout.addSpacing(4)

        # Add buttons
        self.button_generate = QPushButton('Generate DB', self)
        self.button_generate.clicked.connect(self.conductGeneration)

        self.button_read = QPushButton('Read DB', self)
        self.button_read.clicked.connect(self.conductRead)

        self.button_drop = QPushButton('Drop DB', self)
        self.button_drop.clicked.connect(self.conductDrop)

        # Add style to buttons
        style_buttons(self)

        # Add buttons to layout
        left_layout.addWidget(self.button_generate)
        left_layout.addWidget(self.button_drop)
        left_layout.addWidget(self.button_read)

        # Add left layout to main layout
        self.layout.addLayout(left_layout)

        # Add a QTableWidget to the right
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        # Set the central widget
        self.setCentralWidget(self.widget)

        # Set the window style
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(203, 223, 247))
        self.setPalette(palette)

        # Make the last column stretch to fill the table
        self.table.horizontalHeader().setStretchLastSection(True)
        style_table(self)
        style_label(self)
        # Load data into the table
        self.load_data()

    def load_data(self):
        with open(self.my_file, 'r') as f:
            lines = f.readlines()

        self.table.setRowCount(len(lines))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Key", "Value"])

        for i, line in enumerate(lines):
            number, string = line.strip().split(' ')
            self.table.setItem(i, 0, QTableWidgetItem(number))
            self.table.setItem(i, 1, QTableWidgetItem(string))

        # Resize columns to fit content
        self.table.resizeColumnsToContents()

        # Set the height of the table such that only 25 rows are visible at a time
        row_height = self.table.rowHeight(0)
        table_height = row_height * 15
        self.table.setFixedHeight(table_height)

    def conductSearch(self):
        self.load_data()
        text = self.value_input.text()
        if text:  # checks if text is not empty
            key = int(text)
            result = self.B.search(key)

            if result is None:
                QMessageBox.warning(self, "Search Result", f"Value be key {key} not found!")
            else:
                # Find the row index of the result value
                row = -1
                for i in range(self.table.rowCount()):
                    item = self.table.item(i, 0)
                    if item.text() == str(key):
                        row = i
                        break

                if row != -1:
                    # Highlight the entire row in the table
                    for column in range(self.table.columnCount()):
                        item = self.table.item(row, column)
                        item.setBackground(QColor(255, 255, 0))

                    # Optionally, you can scroll to the highlighted item
                    self.table.scrollToItem(self.table.item(row, 0))
                    self.lcd_number.display(self.B.getNumOfComparisons)
                    # Unhighlight the item after 5 seconds
                    QTimer.singleShot(5000, lambda: self.unhighlightItem(row))
        else:
            QMessageBox.warning(self, "Search Result", "Field is empty!")

    def unhighlightItem(self, row):
        for column in range(self.table.columnCount()):
            item = self.table.item(row, column)
            if item is not None:  # Check if the item is not None
                item.setBackground(QColor(255, 255, 255))

    def conductInsertion(self):
        self.load_data()
        text = self.value_input.text()
        if text:  # checks if text is not empty
            text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your string:')

            if ok:
                string = text
                key = int(self.value_input.text())
                self.B.insert(key, string)
                with open(self.my_file, 'a') as f:  # Open in append mode
                    f.write(f'{key} {string}\n')
                self.load_data()
        else:
            QMessageBox.warning(self, "Insertion Result", "Field is empty!")

    def conductDeletion(self):
        self.load_data()
        text = self.value_input.text()
        if text:  # checks if text is not empty
            key = int(text)
            if self.B.search(key):
                self.B.delete(self.B.root, int(key))
                self.delete_from_file(str(key))
                self.load_data()
            else:
                QMessageBox.warning(self, "Deletion Result", f"Value be key {key} not found!")
        else:
            QMessageBox.warning(self, "Deletion Result", "Field is empty!")

    def delete_from_file(self, pattern):
        # Read the file into a list of lines
        with open(self.my_file, 'r') as file:
            lines = file.readlines()

        # Find lines that start with the pattern followed by a space
        matching_lines = [line for line in lines if line.startswith(str(pattern) + ' ')]
        lines = [line for line in lines if not line.startswith(str(pattern) + ' ')]

        # Write the updated contents back to the file
        with open(self.my_file, 'w') as file:
            file.writelines(lines)

        if matching_lines:
            print(f"Lines starting with '{pattern}' deleted successfully.")
        else:
            print(f"No lines starting with '{pattern}' found.")

    def conductModification(self):
        self.load_data()
        text = self.value_input.text()
        if text:  # checks if text is not empty
            key = int(text)
            new_value, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your new string:')

            if ok:
                # Check if the key exists in the B-tree
                if self.B.search(key):
                    # Update the value in the B-tree
                    self.B.update(key, new_value)

                    # Update the value in the file
                    self.update_in_file(str(key), new_value)

                    # Reload the data in table
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Search Result", f"Value with key {key} not found!")
        else:
            QMessageBox.warning(self, "Deletion Result", "Field is empty!")

    def update_in_file(self, key, new_value):
        # Read the file into a list of lines
        with open(self.my_file, 'r') as file:
            lines = file.readlines()

        # Update the line that starts with the key followed by a space
        for i in range(len(lines)):
            if lines[i].startswith(str(key) + ' '):
                lines[i] = f'{key} {new_value}\n'
                break

        # Write the updated contents back to the file
        with open(self.my_file, 'w') as file:
            file.writelines(lines)

    def conductGeneration(self):
        new_value, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your new DB name and size:')
        if ok and new_value:  # checks if user clicked OK and input is not empty
            split_value = new_value.split()
            if len(split_value) == 2:
                self.my_file, n = split_value
                n = int(n)
                generateDB(n, self.my_file, 1, 100000)
                self.B = build_Btree(self.t, self.my_file)
                self.load_data()
            else:
                QMessageBox.warning(self, "Warning!", "Please enter DB name and size separated by a space.")
        else:
            QMessageBox.warning(self, "Warning!", "No input provided.")

    def conductDrop(self):
        with open(self.my_file, 'w') as f:
            pass
        self.load_data()

    def conductRead(self):
        new_value, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your DB name:')
        if ok and new_value:  # checks if user clicked OK and input is not empty
            if os.path.isfile(new_value):
                self.my_file=new_value
                self.B = build_Btree(self.t, self.my_file)
                self.load_data()
            else:
                QMessageBox.warning(self, "Reading from DB", "File does not exist.")
        else:
            QMessageBox.warning(self, "Reading from DB", "No input provided.")


