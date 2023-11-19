from PyQt5.QtWidgets import QPushButton, QTableWidget, QLCDNumber, QLineEdit, QLabel


def style_buttons(widget):
    for button in widget.findChildren(QPushButton):
        button.setFixedSize(180, 48)
        button.setStyleSheet("""
            QPushButton {
                background-color: rgb(154,194,243);
                border: 0px solid #ffff;
                padding: 5px;
                border-radius: 10px;
                width: 120px;
                font-family: 'Noto Sans';
                font-size: 16px; 
            }

            QPushButton:hover, QPushButton:pressed {
                background-color: #bad5dd;
                border: 1px solid #217ce7;
                text-decoration: underline;
                color: #217ce7;
            }
        """)


def style_table(widget):
    for table in widget.findChildren(QTableWidget):
        table.setStyleSheet("""
                QTableWidget {
                    background-color: #ffffff;  # Set table background color
                }
                """)


def style_lcd_number(widget):
    for lcd_number in widget.findChildren(QLCDNumber):
        lcd_number.setFixedSize(180, 36)
        lcd_number.setStyleSheet("""
                        QLCDNumber {
                            background-color: rgb(154, 194, 243);
                            color:royalblue;
                            border: 1px solid royalblue;
                            border-radius: 5px;
                        }
                    """)


def style_value_input(widget):
    for qLine in widget.findChildren(QLineEdit):
        qLine.setFixedSize(180, 46)
        qLine.setStyleSheet("""
            QLineEdit {
                background-color: rgb(255, 255, 255);
                border: 1px solid rgb(154, 194, 243);
                border-radius: 5px;
                padding: 5px;
                font-size: 18px;
                font-family: 'Noto Sans';
            }

            QLineEdit:focus {
                border: 2px solid rgb(72, 118, 255);
            }
        """)


def style_label(widget):
    for qLabels in widget.findChildren(QLabel):
        qLabels.setStyleSheet("""
                    QLabel {
                        font-family: 'Noto Sans';
                        font-size: 16px;
                    }
                """)
