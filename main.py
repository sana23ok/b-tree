import sys
from PyQt5.QtWidgets import QApplication
from generation import generateDB
from build_tree import build_Btree
from pyUI import MainWindow

n = 30
name = 'db.txt'
# generateDB(n, name, 1, 100)
t=10
B=build_Btree(t, name)

# if __name__ == "__main__":
app = QApplication(sys.argv)
main = MainWindow(B)
main.show()
sys.exit(app.exec_())

