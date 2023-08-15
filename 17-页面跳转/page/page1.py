from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit
from page.page2 import Page2


class Page1(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.button_list = ['2']

        self.initUI()

    def initUI(self):
        # 创建垂直布局
        layout = QVBoxLayout()

        layout.addWidget(QLineEdit('page1'))

        # 根据按钮列表生成按钮
        for button_text in self.button_list:
            if button_text == '1':
                button = QPushButton(button_text)
                button.clicked.connect(lambda: self.parent.switch_page_by_class('page1'))
            elif button_text == '2':
                button = QPushButton(button_text)
                button.clicked.connect(lambda: self.parent.switch_page_by_class(Page2))
            else:
                button = QPushButton(button_text)
            layout.addWidget(button)

        layout.addWidget(QTextEdit())

        # 将布局设置为窗口的主布局
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    window = Page1()
    window.show()
    app.exec()
