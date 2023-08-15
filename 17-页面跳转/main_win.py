import qtawesome
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QDesktopWidget, QFrame, QHBoxLayout, QPushButton, QWidget, \
    QVBoxLayout

from page.home import Home
from util.stack import Stack
from util.ui_manage import UiManager


class MainWin(QMainWindow):

    def __init__(self):
        super().__init__()
        UiManager.add_page('MainWin', self)
        # 创建堆栈控件
        self.stacked_widget = QStackedWidget()
        self.set_default_size()
        self.center()
        self.move_flag = False  # 移动事件标志位
        self.point = None  # 起始点坐标

        # 用栈来存储所有页面
        self.stack = Stack()
        self.init_page()

    def set_default_size(self):
        """
        设置默认尺寸
        :return:
        """
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * (3 / 4))
        height = int(screen.height() * (3 / 4))
        size = QSize(width, height)
        self.resize(size)

    def center(self):
        """
        界面居中
        :return:
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
                  int((screen.height() - size.height()) / 2))

    def init_page(self):
        """
        初始化页面
        :return:
        """
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏标题栏
        page = CustomWidget(self, Home(self))
        self.stacked_widget.addWidget(page)
        self.stack.push(page)
        self.setCentralWidget(self.stacked_widget)

    def switch_page_by_class(self, _class, *args, **kwargs):
        """
        根据页面类跳转页面
        :param _class: 页面对应的类
        :param args:
        :param kwargs:
        :return:
        """
        page = CustomWidget(self, _class(self, *args, **kwargs))
        self.stacked_widget.insertWidget(0, page)
        # 当页面到达首页时，清空栈
        if _class == Home:
            # 销毁页面
            for del_page in self.stack.items:
                del_page.deleteLater()
            self.stack = Stack()
        self.stack.push(page)
        self.stacked_widget.setCurrentIndex(0)

    def back(self):
        """
        返回上一级
        :return:
        """
        if self.stack.size() > 1:
            self.stack.pop()
            page = self.stack.peek()
            self.stacked_widget.insertWidget(0, page)
            self.stacked_widget.setCurrentIndex(0)


class CustomWidget(QWidget):

    def __init__(self, parent, content_frame):
        super().__init__()
        self.parent = parent
        self.main_layout = QVBoxLayout()
        self.top_frame = TopFrame(self.parent)
        self.content_frame = content_frame
        self.init_ui()

    def init_ui(self):
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.top_frame, 1)
        self.main_layout.addWidget(self.content_frame, 14)
        self.setLayout(self.main_layout)


class TopFrame(QFrame):
    """
    标题栏
    重写了 缩小、放大/还原、关闭、拖动、双击放大/还原
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.this_layout = QHBoxLayout()
        self.back_icon = QPushButton(qtawesome.icon('msc.debug-step-back'), '')  # 返回
        self.home_icon = QPushButton(qtawesome.icon('mdi6.home'), '')  # 主页
        self.min_icon = QPushButton(qtawesome.icon('msc.chrome-minimize'), '')  # 最小化
        self.max_icon = QPushButton(qtawesome.icon('msc.chrome-restore'), '')  # 最大化
        self.close_icon = QPushButton(qtawesome.icon('msc.chrome-close'), '')  # 关闭
        self.init_ui()
        self.init_connect()

    def init_ui(self):
        # 设置顶部图标与两侧距离
        self.setContentsMargins(20, 0, 0, 0)
        self.set_back_icon()
        self.set_home_icon()
        self.set_min_icon()
        self.set_max_icon()
        self.set_close_icon()
        self.this_layout.addStretch(1)
        self.this_layout.addWidget(self.back_icon)
        self.this_layout.addWidget(self.home_icon)
        self.this_layout.addWidget(self.min_icon)
        self.this_layout.addWidget(self.max_icon)
        self.this_layout.addWidget(self.close_icon)
        self.setLayout(self.this_layout)

    def init_connect(self):
        self.back_icon.clicked.connect(self.back_button_click)
        self.home_icon.clicked.connect(self.home_button_click)
        self.min_icon.clicked.connect(self.min_button_click)
        self.max_icon.clicked.connect(self.max_button_click)
        self.close_icon.clicked.connect(self.close_button_click)

    def quit_app(self):
        self.parent.close()

    def set_back_icon(self):
        self.back_icon.setObjectName("BackIcon")
        self.back_icon.setMinimumSize(QSize(30, 30))
        self.back_icon.setMaximumSize(QSize(30, 30))

    def set_home_icon(self):
        self.home_icon.setObjectName("HomeIcon")
        self.home_icon.setMinimumSize(QSize(30, 30))
        self.home_icon.setMaximumSize(QSize(30, 30))

    def set_min_icon(self):
        self.min_icon.setObjectName("MinIcon")
        self.min_icon.setMinimumSize(QSize(30, 30))
        self.min_icon.setMaximumSize(QSize(30, 30))

    def set_max_icon(self):
        self.max_icon.setObjectName("MaxIcon")
        self.max_icon.setMinimumSize(QSize(30, 30))
        self.max_icon.setMaximumSize(QSize(30, 30))

    def set_close_icon(self):
        self.close_icon.setObjectName("CloseIcon")
        self.close_icon.setMinimumSize(QSize(30, 30))
        self.close_icon.setMaximumSize(QSize(30, 30))

    def back_button_click(self):
        """
        返回上一级
        :return:
        """
        self.parent.back()

    def home_button_click(self):
        """
        返回首页
        :return:
        """
        self.parent.switch_page_by_class(Home)

    def min_button_click(self):
        """
        最小化窗口
        :return:
        """
        if isinstance(self, QMainWindow) or isinstance(self, QFrame):
            self.parent.showMinimized()

    def max_button_click(self):
        """
        最大化窗口/还原窗口
        :return:
        """
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def close_button_click(self):
        """
        关闭窗口
        :return:
        """
        self.quit_app()

    def mouseDoubleClickEvent(self, event):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.parent.move_flag = True
            self.parent.point = event.globalPos() - self.parent.pos()  # 记录起始点坐标
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if Qt.LeftButton and self.parent.move_flag:
            self.parent.move(event.globalPos() - self.parent.point)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.parent.move_flag = False
