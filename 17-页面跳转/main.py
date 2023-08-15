from PyQt5.QtWidgets import QApplication
from main_win import MainWin

if __name__ == '__main__':
    app = QApplication([])
    window = MainWin()
    window.show()
    app.exec()
