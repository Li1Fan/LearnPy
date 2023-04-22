# 通用模板
import sys
import qtawesome as qta
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QPushButton, QGridLayout, QApplication


class Example(QWidget):  # 可以选择QWidge或者QMainWindow作为基类
    def __init__(self):
        super(Example, self).__init__()  # 继承基类
        self.init()
        self.init_widget()
        self.set_layout()

    def init(self):
        self.resize(1000, 750)  # 大小

        screen = QDesktopWidget().screenGeometry()  # 屏幕几何的大小
        window = self.geometry()  # 窗口的大小
        self.move((screen.width() - window.width()) // 2, (screen.height() - window.height()) // 2)  # 移动至屏幕中间

        self.setWindowTitle('title')  # 标题

    def init_widget(self):
        self.btn = QPushButton()
        self.btn.setIcon(qta.icon('fa.eye'))

    def set_layout(self):
        grid = QGridLayout()
        grid.addWidget(self.btn, 0, 0, 1, 1)

        grid.setColumnStretch(0, 1)
        self.setLayout(grid)


def main():
    app = QApplication(sys.argv)  # 创建应用程序对象，sys.argv是一个命令行参数列表
    w = Example()  # 创建实例对象
    w.show()
    sys.exit(app.exec_())  # 进入程序的主循环，遇到退出情况，终止程序


if __name__ == "__main__":  # 主程序才运行
    main()
