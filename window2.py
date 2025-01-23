from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from sqlite3 import connect
class SYSWIN(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Login")
        self.resize(756, 488)
        self.setWindowIcon(QIcon('image.png'))
        print(self.name)

def main():
    app = QApplication([])
    window = SYSWIN("name")
    window.show()
    app.exec_()
if __name__ == "__main__":
    main()
