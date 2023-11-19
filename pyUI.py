from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QPushButton, QHBoxLayout, QLineEdit, QLabel, QLCDNumber, QMessageBox
from setStyles import style_buttons, style_table, style_lcd_number, style_value_input, style_label
from b_tree import BTree


class MainWindow(QMainWindow):
    def __init__(self, tree: BTree, file='db.txt', parent=None):
        super(MainWindow, self).__init__(parent)
        self.widget = QWidget(self)
        self.layout = QHBoxLayout(self.widget)
        # self.resize(600, self.sizeHint().height())
        self.my_file = file
        self.B = tree
        self.B.print_tree(self.B.root)
        self.layout.setContentsMargins(40, 20, 20, 20)

        # Left side layout (labels, buttons, and text field)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 10, 80, 10)
        # Add labels
        label_value = QLabel("Value", self)
        left_layout.addWidget(label_value)

        # Add a QLineEdit for entering values
        self.value_input = QLineEdit(self)
        self.value_input.setPlaceholderText("Enter a value")
        style_value_input(self)
        left_layout.addWidget(self.value_input)

        # Add buttons
        self.button_insert = QPushButton('Insert', self)
        self.button_delete = QPushButton('Delete', self)
        self.button_search = QPushButton('Search', self)
        self.button_search.clicked.connect(self.conductSearch)
        self.button_modify = QPushButton('Modify', self)

        # Add style to buttons
        style_buttons(self)

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

        # Add three QLabel and QLineEdit pairs
        for i in range(3):
            # Add labels
            label_value = QLabel(f"Value{i + 1}", self)
            left_layout.addWidget(label_value)
            lcd_number = QLCDNumber(self)
            left_layout.addWidget(lcd_number)

        style_lcd_number(self)

        # Add a margin below buttons
        left_layout.addSpacing(4)

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
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Value"])

        for i, line in enumerate(lines):
            self.table.setItem(i, 0, QTableWidgetItem(line.strip()))

        # Resize columns to fit content
        self.table.resizeColumnsToContents()

        # Set the height of the table such that only 25 rows are visible at a time
        row_height = self.table.rowHeight(0)
        table_height = row_height * 15
        self.table.setFixedHeight(table_height)

    def conductSearch(self):
        value = int(self.value_input.text())
        result = self.B.search(value)

        if result is None:
            QMessageBox.warning(self, "Search Result", f"Value {value} not found!")
        else:
            # Find the row index of the result value
            row = -1
            for i in range(self.table.rowCount()):
                item = self.table.item(i, 0)
                if item.text() == str(value):
                    row = i
                    break

            if row != -1:
                # Highlight the entire row in the table
                for column in range(self.table.columnCount()):
                    item = self.table.item(row, column)
                    item.setBackground(QColor(255, 255, 0))  # Set a custom background color

                # Optionally, you can scroll to the highlighted item
                self.table.scrollToItem(self.table.item(row, 0))
