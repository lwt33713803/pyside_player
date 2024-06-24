import os

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QMouseEvent, QPixmap, QIcon
from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QStatusBar
from utils.helpers import load_stylesheet, get_assets_path


class HoverAbleHBoxLayout(QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            obj.setStyleSheet("background-color: yellow;")
        elif event.type() == QEvent.Type.Leave:
            obj.setStyleSheet("background-color: red;")
        return super().eventFilter(obj, event)


class UiMainWindow(object):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self):
        self.openHistoryWidget = None
        self.openUrlWidget = None
        self.fileT = None

    def setupUi(self, MainWindow):
        # qss
        MainWindow.setStyleSheet(load_stylesheet("assets/styles/start.qss"))
        MainWindow.setFixedSize(640, 400)
        MainWindow.setObjectName("main_window")

        mainWindowWeight = QWidget(parent=MainWindow)
        mainWindowWeight.setObjectName("main_widget")

        hLayout = QHBoxLayout(mainWindowWeight)
        hLayout.setObjectName("main_layout")
        hLayout.setContentsMargins(0, 0, 0, 0)

        # 创建左侧部件
        left_widget = QWidget(parent=mainWindowWeight)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.setContentsMargins(20, 20, 20, 20)

        left_widget.setObjectName("left_panel")
        left_layout.setObjectName("left_layout")

        # 创建右侧部件
        right_widget = QWidget(parent=mainWindowWeight)
        right_layout = QVBoxLayout(right_widget)
        right_widget.setObjectName("right_panel")
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_layout.setContentsMargins(20, 40, 20, 20)
        right_layout.setObjectName("right_layout")

        # 将左右部件添加到主布局中
        hLayout.addWidget(left_widget)
        hLayout.addWidget(right_widget)
        hLayout.setStretch(0, 1)
        hLayout.setStretch(1, 2)

        # 左侧布局组件
        logo = QLabel(parent=mainWindowWeight)
        logo.setObjectName("label")
        image_path = os.path.join(get_assets_path(), "images/logo.jpg")
        pixmap = QPixmap(image_path)
        width, height = 100, 100
        scaled_pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setPixmap(scaled_pixmap)
        logo.setFixedHeight(150)
        logo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        title = QLabel(parent=mainWindowWeight)
        title.setObjectName("title")
        title.setText("引力播放器")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version = QLabel(parent=mainWindowWeight)
        version.setObjectName("version")
        version.setText("24.06.04")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_layout.addWidget(logo)
        left_layout.addWidget(title)
        left_layout.addWidget(version)

        # 右侧布局组件
        openWidget = QPushButton(parent=mainWindowWeight)
        openLayout = QHBoxLayout(openWidget)
        openWidget.setObjectName("open_widget")
        openWidget.setContentsMargins(0, 0, 0, 0)
        openWidget.setFixedHeight(40)
        openWidget.clicked.connect(self.picker)

        self.openUrlWidget = QPushButton(parent=mainWindowWeight)
        openUrlLayout = QHBoxLayout(self.openUrlWidget)
        self.openUrlWidget.setObjectName("open_url_widget")
        self.openUrlWidget.setContentsMargins(0, 0, 0, 0)
        self.openUrlWidget.setFixedHeight(40)
        right_layout.setSpacing(0)
        self.openHistoryWidget = QWidget(parent=mainWindowWeight)
        openHistoryLayout = HoverAbleHBoxLayout(self.openHistoryWidget)
        self.openHistoryWidget.setObjectName("open_history_widget")

        right_layout.addWidget(openWidget)
        right_layout.addWidget(self.openUrlWidget)
        right_layout.addWidget(self.openHistoryWidget)

        openText = QLabel(parent=mainWindowWeight)
        openText.setObjectName("title_open_local")
        openText.setText("打开...")
        openText.setStyleSheet("font-size:12px;font-weight:normal;color:#ffffff")
        openText.setAlignment(Qt.AlignmentFlag.AlignLeft)

        openTextHotkey = QLabel(parent=mainWindowWeight)
        openTextHotkey.setObjectName("title_open_local_hotkey")
        openTextHotkey.setText("COMMAND + O")
        openTextHotkey.setAlignment(Qt.AlignmentFlag.AlignRight)

        openLayout.setAlignment(Qt.AlignmentFlag.AlignBaseline)
        openLayout.addWidget(openText)
        openLayout.addWidget(openTextHotkey)

        openUrlText = QLabel(parent=mainWindowWeight)
        openUrlText.setObjectName("title_open_url")
        openUrlText.setText("打开 URL...")
        openUrlText.setAlignment(Qt.AlignmentFlag.AlignLeft)

        openUrlTextHotkey = QLabel(parent=mainWindowWeight)
        openUrlTextHotkey.setObjectName("title_open_local_hotkey")
        openUrlTextHotkey.setText("SHIFT + CTRL + O")
        openUrlTextHotkey.setAlignment(Qt.AlignmentFlag.AlignRight)

        openUrlLayout.addWidget(openUrlText)
        openUrlLayout.addWidget(openUrlTextHotkey)
        openUrlLayout.setAlignment(Qt.AlignmentFlag.AlignBaseline)

        openItemIcon = QLabel(parent=mainWindowWeight)
        openItemIcon.setObjectName("open_item_icon")
        open_item_icon_path = os.path.join(get_assets_path(), "icons/files.png")
        open_item_pixmap = QPixmap(open_item_icon_path)
        open_item_scaled_pixmap = open_item_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio,
                                                          Qt.TransformationMode.SmoothTransformation)

        openItemIcon.setPixmap(open_item_scaled_pixmap)
        openItemIcon.setFixedHeight(20)
        openItemIcon.setFixedWidth(20)
        openItemIcon.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        openItemWidget = QLabel(parent=mainWindowWeight)
        openItemWidget.setObjectName("title_open_history_item")
        openItemWidget.setText("Download")

        openHistoryLayout.addWidget(openItemIcon)
        openHistoryLayout.addWidget(openItemWidget)
        openHistoryLayout.setObjectName("open_history_item")
        self.openHistoryWidget.setContentsMargins(0, 0, 0, 0)

        # 隐藏标题栏目等操作
        MainWindow.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        MainWindow.setCentralWidget(mainWindowWeight)
        MainWindow.setWindowOpacity(0.99)
        MainWindow.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setUpButtons(MainWindow)

    @staticmethod
    def setUpButtons(MainWindow):
        # 菜单按钮
        # 添加关闭按钮
        icon_close = QPixmap(os.path.join(get_assets_path(), "icons/close.png"))
        close_button = QPushButton(parent=MainWindow)
        close_button.clicked.connect(MainWindow.close)
        close_button.setIcon(QIcon(icon_close))
        close_button.setObjectName("close_btn")
        close_button.setGeometry(600, 0, 40, 40)

        # 添加最小化按钮
        icon_min = QIcon(os.path.join(get_assets_path(), "icons/min.png"))
        minimize_button = QPushButton(parent=MainWindow)
        minimize_button.clicked.connect(MainWindow.showMinimized)
        minimize_button.setIcon(icon_min)
        minimize_button.setObjectName("mini_btn")
        minimize_button.setGeometry(560, 0, 40, 40)

    @staticmethod
    def picker(self):
        filenames, filetype = QtWidgets.QFileDialog.getOpenFileNames(None, "选取文件夹")  # 起始路径
        if len(filenames) == 0:
            print("取消选择")
            return
        files = []
        for filename in filenames:
            files.append(filename)
        print('\n'.join(files))

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton:
            self._isTracking = True
            self._startPos = e.pos()

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None
