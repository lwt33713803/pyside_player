import os.path

from PySide6 import QtCore
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QIcon, QPixmap, QTransform, QGuiApplication
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedLayout, QSizePolicy, QHBoxLayout, QLabel, \
    QSlider, QSpacerItem

from player.playerController import PlayerController
from utils.helpers import load_stylesheet, get_assets_path


class UiMainWindow(object):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self):
        super().__init__()
        self.optionButtonGroup = None
        self.actionButtonGroupPlay = None
        self.voiceSlider = None
        self.voiceIcon = None
        self.voiceButtonGroup = None
        self.actionButtonGroup = None
        self.slider = None
        self.drag_position = None
        self.mouse_has_moved = None
        self.start_pos = None
        self.end_pos = None
        self.statePanelWidgetStateTextSubtitle = None
        self.statePanelWidgetStateTextTitle = None
        self.stateIcon = None
        self.is_mouse_pressed = None
        self.titlebarTitle = None
        self.mainWindowWeight = None
        self.tabs = None
        self.state = None
        self.titlebar = None
        self.player = None
        self.controller = None
        self.videoContainerWidget = None
        self._player = None
        self._audio_output = None

    def setupUi(self, MainWindow):
        # QSS
        MainWindow.setStyleSheet(load_stylesheet("assets/styles/player.qss"))
        MainWindow.resize(1200, 800)
        MainWindow.setObjectName("player_window")
        ## 主要容器widget
        self.mainWindowWeight = QWidget(parent=MainWindow)
        self.mainWindowWeight.setObjectName("mainWidget")
        MainWindow.setCentralWidget(self.mainWindowWeight)

        videoWidgetContainer = QWidget(self.mainWindowWeight)
        videoWidgetLayout = QHBoxLayout(videoWidgetContainer)

        videoWidgetContainer.lower()
        ## 视频widget
        self.videoWidget = QVideoWidget(self.mainWindowWeight)
        self.videoWidget.setFixedSize(600, 400)
        self.videoWidget.setStyleSheet("background-color: rgb(0, 255, 255);")
        videoWidgetLayout.addWidget(self.videoWidget)
        self.videoWidget.lower()
        videoWidgetContainer.move(100,10)

        self.controller = PlayerController(self.mainWindowWeight)
        self.controller.setFixedSize(500, 130)
        self.controller.setStyleSheet("background-color: rgba(0, 0, 0,0.8);")
        self.controller.setObjectName("controllerPanel")
        self.controller.move(350, 650)
        self.controllerLayout = QVBoxLayout(self.controller)
        self.controllerLayout.setContentsMargins(0, 0, 0, 20)

        demoButton = QPushButton(self.mainWindowWeight)
        demoButton.setFixedSize(100, 35)
        demoButton.setText("选择视频文件")
        demoButton.setStyleSheet("background-color: rgb(0, 255, 255);")
        demoButton.move(50,250)

        # 组件1 顶部菜单栏
        self.buildTitleBar(MainWindow)
        # 组件2 控制器
        self.buildVideoController()
        # 组件3 状态显示
        self.buildStatePanel()

        self.controllerLayout.setSpacing(0)
        self.controllerLayout.setContentsMargins(0, 0, 0, 0)

        # 其他
        MainWindow.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    # 状态管理
    def buildStatePanel(self):
        self.state = QWidget(self.mainWindowWeight)
        self.state.setFixedSize(320, 100)
        self.state.move(10, 40)
        stateLayout = QHBoxLayout(self.state)
        statePanelWidget = QWidget(self.mainWindowWeight)
        statePanelWidget.setFixedSize(300, 100)
        statePanelWidget.setStyleSheet("background-color: rgba(0, 0, 0,0.4);border-radius: 4px;")
        stateLayout.addWidget(statePanelWidget)
        stateLayout.setSpacing(0)
        statePanelWidgetLayout = QHBoxLayout(statePanelWidget)
        statePanelWidgetStateIcon = QLabel()
        statePanelWidgetStateIcon.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        statePanelWidgetStateIcon.setFixedWidth(80)
        self.stateIcon = QPixmap(os.path.join(get_assets_path(), 'icons/play.png')).scaled(QSize(70, 70))
        statePanelWidgetStateIcon.setPixmap(self.stateIcon)
        statePanelWidgetStateIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        statePanelWidgetLayout.addWidget(statePanelWidgetStateIcon)
        statePanelWidgetStateText = QWidget(statePanelWidget)
        statePanelWidgetStateText.setStyleSheet("background-color:transparent;")
        statePanelWidgetLayout.addWidget(statePanelWidgetStateText)
        statePanelWidgetStateTextLayout = QVBoxLayout(statePanelWidgetStateText)
        self.statePanelWidgetStateTextTitle = QLabel()
        self.statePanelWidgetStateTextSubtitle = QLabel()
        statePanelWidgetStateTextLayout.addWidget(self.statePanelWidgetStateTextTitle)
        statePanelWidgetStateTextLayout.addWidget(self.statePanelWidgetStateTextSubtitle)
        self.statePanelWidgetStateTextTitle.setText("暂停")
        self.statePanelWidgetStateTextTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statePanelWidgetStateTextTitle.setStyleSheet("font-size:18px;color:#ffffff;background-color:transparent;")
        self.statePanelWidgetStateTextSubtitle.setText("00:11:10 / 11:11:11"),
        self.statePanelWidgetStateTextSubtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statePanelWidgetStateTextSubtitle.setStyleSheet(
            "font-size:14px;color:#cccccc;background-color:transparent;")

        stateLayout.setContentsMargins(10, 0, 0, 0)
        stateLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.state.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.state.setFixedHeight(120)

    # 视频控制器
    def buildVideoController(self):

        actions = QWidget()
        actions.setFixedSize(500, 100)

        actionsLayout = QVBoxLayout(actions)
        actionsLayout.setContentsMargins(15, 10, 15, 10)
        actionsLayout.setSpacing(0)

        actionButtons = QWidget(self.mainWindowWeight)
        actionButtons.setStyleSheet("background-color: rgba(0, 0, 0,0);")
        actionButtons.setFixedSize(470, 60)
        actionButtonsLayout = QHBoxLayout(actionButtons)
        actionButtonsLayout.setContentsMargins(0, 0, 0, 0)
        actionButtonsLayout.setSpacing(30)
        # 组件2 控制器 - 音量组件
        self.voiceButtonGroup = QWidget(self.mainWindowWeight)
        voiceButtonGroupLayout = QHBoxLayout(self.voiceButtonGroup)
        voiceButtonGroupLayout.setContentsMargins(0, 0, 0, 0)
        self.voiceButtonGroup.setFixedWidth(100)
        self.voiceIcon = QPushButton()
        self.voiceIcon.setIconSize(QSize(20, 20))
        self.voiceIcon.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/volume-up.png'))))
        voiceButtonGroupLayout.addWidget(self.voiceIcon)

        self.voiceSlider = QSlider(Qt.Orientation.Horizontal)
        self.voiceSlider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.voiceSlider.setFixedHeight(5)
        voiceButtonGroupLayout.addWidget(self.voiceSlider)

        # 组件2 控制器 - 音量先组件 播放 暂停，上下
        self.actionButtonGroup = QWidget(self.mainWindowWeight)
        actionButtonGroupLayout = QHBoxLayout(self.actionButtonGroup)
        actionButtonGroupLayout.setContentsMargins(0, 0, 0, 0)
        actionButtonGroupLayout.setSpacing(0)
        actionButtonGroupPrev = QPushButton(self.mainWindowWeight)
        transform = QTransform()
        transform.rotate(180)
        actionButtonGroupPrev.setIcon(
            QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/arr.png')).transformed(transform)))
        actionButtonGroupPrev.setIconSize(QSize(30, 30))
        actionButtonGroupPrev.setFixedSize(60, 60)

        self.actionButtonGroupPlay = QPushButton(self.mainWindowWeight)
        self.actionButtonGroupPlay.setContentsMargins(0, 0, 0, 0)
        playIcon = QPixmap(os.path.join(get_assets_path(), 'icons/play.png'))
        playIcon.scaled(60, 60)
        self.actionButtonGroupPlay.setIcon(QIcon(playIcon))
        self.actionButtonGroupPlay.setIconSize(QSize(50, 50))
        self.actionButtonGroupPlay.setFixedSize(60, 60)

        actionButtonGroupNest = QPushButton(self.mainWindowWeight)
        actionButtonGroupNest.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/arr.png'))))
        actionButtonGroupNest.setIconSize(QSize(30, 30))
        actionButtonGroupNest.setFixedSize(60, 60)

        actionButtonGroupLayout.addWidget(actionButtonGroupPrev)
        actionButtonGroupLayout.addWidget(self.actionButtonGroupPlay)
        actionButtonGroupLayout.addWidget(actionButtonGroupNest)

        # 组件2 控制器 - 设置 播放列表，音轨视轨字幕
        self.optionButtonGroup = QWidget(self.mainWindowWeight)
        self.optionButtonGroup.setFixedWidth(100)
        optionButtonGroupLayout = QHBoxLayout(self.optionButtonGroup)

        optionButtonGroupLock = QPushButton(self.mainWindowWeight)
        optionButtonGroupLock.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/lock.png'))))
        optionButtonGroupLock.setIconSize(QSize(18, 18))
        optionButtonGroupLayout.addWidget(optionButtonGroupLock)

        optionButtonGroupMenu = QPushButton(self.mainWindowWeight)
        optionButtonGroupMenu.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/menu.png'))))
        optionButtonGroupMenu.setIconSize(QSize(18, 18))
        optionButtonGroupMenu.clicked.connect(self.on_menu_press)
        optionButtonGroupLayout.addWidget(optionButtonGroupMenu)

        optionButtonGroupSettings = QPushButton(self.mainWindowWeight)
        optionButtonGroupSettings.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/settings.png'))))
        optionButtonGroupSettings.setIconSize(QSize(18, 18))
        optionButtonGroupLayout.addWidget(optionButtonGroupSettings)

        actionButtonsLayout.addWidget(self.voiceButtonGroup)
        actionButtonsLayout.addWidget(self.actionButtonGroup)
        actionButtonsLayout.addWidget(self.optionButtonGroup)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setStyleSheet("background-color: rgba(0, 0, 0,0);")
        self.slider.setFixedSize(470, 20)
        self.slider.setCursor(Qt.CursorShape.DragMoveCursor)

        self.slider.setTickPosition(QSlider.TickPosition.NoTicks)

        actionsLayout.addWidget(actionButtons)
        actionsLayout.addWidget(self.slider)

        self.controllerLayout.addWidget(actions)
        self.controllerLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)


    # 标题栏
    def buildTitleBar(self,MainWindow):
        self.titlebar = QWidget(self.mainWindowWeight)
        self.titlebar.setFixedSize(MainWindow.width(), 30)
        self.titlebar.setObjectName("titleBar")
        titlebarLayout = QHBoxLayout(self.titlebar)
        titlebarLayout.setContentsMargins(0, 0, 0, 10)
        # 组件1 - part1 标题
        self.titlebarTitle = QLabel(self.mainWindowWeight)
        self.titlebarTitle.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.titlebarTitle.setFixedHeight(30)
        self.titlebarTitle.setText("当前播放电影的名字.mp4")
        self.titlebarTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titlebarLayout.addWidget(self.titlebarTitle)
        self.titlebarTitle.setObjectName("titlebarTitle")
        titlebarLayout.setSpacing(0)
        # 组件1 - part2 最小化
        titlebarMinScreenButton = QPushButton(self.mainWindowWeight)
        titlebarMinScreenButton.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/min.png'))))
        titlebarMinScreenButton.setFixedSize(30, 30)
        titlebarMinScreenButton.setObjectName("min_button")
        titlebarMinScreenButton.clicked.connect(self.minPlayerWindows)
        titlebarLayout.addWidget(titlebarMinScreenButton)
        # 组件1 - part2 全屏
        titlebarFullScreenButton = QPushButton(self.mainWindowWeight)
        titlebarFullScreenButton.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/full.png'))))
        titlebarFullScreenButton.setFixedSize(30, 30)
        titlebarFullScreenButton.setObjectName("full_button")
        titlebarFullScreenButton.clicked.connect(self.maxPlayerWindows)
        titlebarLayout.addWidget(titlebarFullScreenButton)
        # 组件1 - part2 关闭
        titlebarCloseButton = QPushButton(self.mainWindowWeight)
        titlebarCloseButton.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/close.png'))))
        titlebarCloseButton.setFixedSize(30, 30)
        titlebarCloseButton.setObjectName("close_button")
        titlebarCloseButton.clicked.connect(self.closePlayerWindows)
        titlebarLayout.addWidget(titlebarCloseButton)

    def minPlayerWindows(self):
        pass

    def maxPlayerWindows(self):
        pass

    def closePlayerWindows(self):
        pass

    # def mouseMoveEvent(self, event):
    #     print("Mouse moved on child widget:", event.pos())
    #     # 阻止事件继续传递到父组件
    #     event.ignore()

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         print("组件点击111")
    #         event.accept()

    def optionClick(self):
        pass

    def on_menu_press(self):
        pass
