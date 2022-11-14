import sys

from PIL import ImageGrab, Image
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from pytesseract import pytesseract


class Snipper(QtWidgets.QWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        self.setWindowTitle("TextShot")
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog
        )

        self.is_macos = sys.platform.startswith("darwin")
        if self.is_macos:
            self.setWindowState(self.windowState() | Qt.WindowMaximized)
        else:
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        self.setStyleSheet("background-color: black")
        self.setWindowOpacity(0.3)

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.start, self.end = QtCore.QPoint(), QtCore.QPoint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QtWidgets.QApplication.quit()

        return super().keyPressEvent(event)

    def paintEvent(self, event):
        if self.start == self.end:
            return super().paintEvent(event)

        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 3))
        painter.setBrush(QtGui.QColor(255, 255, 255, 100))

        if self.is_macos:
            start, end = (self.mapFromGlobal(self.start), self.mapFromGlobal(self.end))
        else:
            start, end = self.start, self.end

        painter.drawRect(QtCore.QRect(start, end))
        return super().paintEvent(event)

    def mousePressEvent(self, event):
        self.start = self.end = QtGui.QCursor.pos()
        self.update()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.end = QtGui.QCursor.pos()
        self.update()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.start == self.end:
            return super().mouseReleaseEvent(event)

        x1, x2 = sorted((self.start.x(), self.end.x()))
        y1, y2 = sorted((self.start.y(), self.end.y()))
        print(x1, x2)
        print(y1, y2)
        shot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        print(type(shot))
        # result = pytesseract.image_to_string(shot)
        result = pytesseract.image_to_string(shot, timeout=2, lang=(sys.argv[1] if len(sys.argv) > 1 else None))
        print(result)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    snipper = Snipper(window)
    snipper.show()
    sys.exit(app.exec_())
    # im = Image.open('code.png')
    # text = pytesseract.image_to_string(im)
    # print(text)