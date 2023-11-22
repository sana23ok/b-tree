import sys
from PyQt5.QtWidgets import QApplication
from pyUI import MainWindow

n = 10000
t = 10

app = QApplication(sys.argv)
main = MainWindow(n, t)
main.show()
sys.exit(app.exec_())

