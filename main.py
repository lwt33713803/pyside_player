import os
import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QSlider, QPushButton, QFileDialog, \
    QHBoxLayout, QFrame, QLabel, QSizePolicy, QGraphicsDropShadowEffect, QLineEdit, QDialog
from PySide6.QtGui import QAction, QPalette, QColor, QIcon, QPixmap, QTransform, QCursor, QDesktopServices
from PySide6.QtCore import Qt, QTimer, QSize, QStandardPaths, QUrl, Signal
from utils.dates import convert_milliseconds_to_time
from utils.helpers import load_stylesheet, get_assets_path
import vlc
import platform
import urllib.parse
import sounddevice as sd


class MediaPlayer(QMainWindow):

    # 初始化
    def __init__(self, master=None):
        super().__init__(master)
        self.url_win = None
        self.stateToast = None
        self.controller_layout = None
        self.timer = None
        self.video_frame = None
        self.h_position_box = None
        self.is_mouse_pressed = None
        self.window_pos = None
        self.mouse_has_moved = None
        self.end_pos = None
        self.start_pos = None
        self.tabPanel = None
        self.positionslider = None
        self.v_box_layout = None
        self.palette = None
        self.widget = None
        self.controller = None
        self.setWindowTitle("引力播放器")
        self.setStyleSheet("background-color: black;")
        self.setMinimumSize(640, 400)
        # vlc instance
        self.instance = vlc.Instance(['-vvv'])
        self.media = None
        # 创建空的媒体播放器
        self.mediaplayer = self.instance.media_player_new()
        self.create_ui()
        self.is_paused = False

    # 菜单
    def buildMenu(self):
        menu_bar = self.menuBar()
        # 菜单
        file_menu = menu_bar.addMenu("文件")
        # 操作栏目
        open_action = QAction("打开视频", self)
        open_action.setShortcut("Ctrl+O")
        open_url_action = QAction("打开URL...", self)
        open_url_action.setShortcut("Ctrl+Shift+O")
        open_url_action.triggered.connect(self.open_url_window)
        open_recent_action = QAction("打开最近文件", self)
        open_history_action = QAction("播放历史", self)
        open_history_action.setShortcut("Ctrl+Alt+H")
        open_delete_current_action = QAction("删除当前文件", self)
        open_save_action = QAction("保留当前播放列表...", self)
        open_history_action = QAction("播放历史", self)
        close_action = QAction("关闭APP", self)
        close_action.setShortcut("Ctrl+W")
        file_menu.addAction(open_action)
        file_menu.addAction(open_url_action)
        file_menu.addAction(open_recent_action)
        file_menu.addSeparator()
        file_menu.addAction(open_history_action)
        file_menu.addSeparator()
        file_menu.addAction(open_delete_current_action)
        file_menu.addAction(open_save_action)
        file_menu.addSeparator()
        file_menu.addAction(close_action)
        open_action.triggered.connect(self.open_file)
        close_action.triggered.connect(sys.exit)

        # 播放
        player_menu = menu_bar.addMenu("播放")
        # 操作栏目
        player_menu_play = QAction("播放", self)
        player_menu_play.setShortcut(Qt.Key.Key_Space)
        player_menu_play.triggered.connect(self.play_pause)
        player_menu.addAction(player_menu_play)
        # 播放速率
        player_rate_menu = player_menu.addMenu("播放速率")
        rate_0_5_action = QAction("0.5 倍", self)
        rate_1_0_action = QAction("1.0 倍", self)
        rate_1_5_action = QAction("1.5 倍", self)
        rate_2_0_action = QAction("2.0 倍", self)
        rate_2_5_action = QAction("2.5 倍", self)
        rate_3_0_action = QAction("3.0 倍", self)
        player_rate_menu.addAction(rate_0_5_action)
        player_rate_menu.addAction(rate_1_0_action)
        player_rate_menu.addAction(rate_1_5_action)
        player_rate_menu.addAction(rate_2_0_action)
        player_rate_menu.addAction(rate_2_5_action)
        player_rate_menu.addAction(rate_3_0_action)
        rate_0_5_action.triggered.connect(lambda: self.set_video_rate(0.5))
        rate_1_0_action.triggered.connect(lambda: self.set_video_rate(1))
        rate_1_5_action.triggered.connect(lambda: self.set_video_rate(1.5))
        rate_2_0_action.triggered.connect(lambda: self.set_video_rate(2.0))
        rate_2_5_action.triggered.connect(lambda: self.set_video_rate(2.5))
        rate_3_0_action.triggered.connect(lambda: self.set_video_rate(3.0))

        player_menu.addSeparator()
        go_shortcut_filters = QAction("前往截图文件夹", self)
        go_shortcut_filters.triggered.connect(self.openShortcutFloder)
        player_menu.addAction(go_shortcut_filters)
        player_menu.addSeparator()
        player_list_menu = player_menu.addMenu("播放列表")

        play_list_01 = QAction("视频1.mp4", self)
        play_list_02 = QAction("视频2.mp4", self)
        play_list_03 = QAction("视频3.mp4", self)
        play_list_04 = QAction("视频4.mp4", self)
        play_list_05 = QAction("视频5.mp4", self)
        play_list_06 = QAction("视频6.mp4", self)
        player_list_menu.addAction(play_list_01)
        player_list_menu.addAction(play_list_02)
        player_list_menu.addAction(play_list_03)
        player_list_menu.addAction(play_list_04)
        player_list_menu.addAction(play_list_05)
        player_list_menu.addAction(play_list_06)

        # playlist_panel = QAction("播放列表", self)
        # playlist_panel.triggered.connect(self.show_play_panel)
        # player_menu.addAction(playlist_panel)

        player_page_menu = player_menu.addMenu("章节列表")
        play_page_01 = QAction("章节1.mp4", self)
        play_page_02 = QAction("章节1.mp4", self)
        play_page_03 = QAction("章节1.mp4", self)
        play_page_04 = QAction("章节1.mp4", self)
        play_page_05 = QAction("章节1.mp4", self)
        play_page_06 = QAction("章节1.mp4", self)
        player_page_menu.addAction(play_page_01)
        player_page_menu.addAction(play_page_02)
        player_page_menu.addAction(play_page_03)
        player_page_menu.addAction(play_page_04)
        player_page_menu.addAction(play_page_05)
        player_page_menu.addAction(play_page_06)
        # playlist_panel = QAction("章节列表", self)
        # player_menu.addAction(playlist_panel)

        # 视频
        video_menu = menu_bar.addMenu("视频")
        # 操作栏目
        open_play_action = QAction("显示视频控制面板", self)
        open_play_action.triggered.connect(self.show_play_panel)
        open_play_action.setShortcut("Ctrl+Shift+L")
        video_route_action = QAction("视频轨道", self)
        video_route_action_change = QAction("循环切换视频轨道", self)
        video_wvh = QAction("长宽比", self)
        video_cj = QAction("裁剪", self)
        video_xz = QAction("旋转", self)
        video_fz = QAction("反转", self)
        video_menu.addAction(open_play_action)
        video_menu.addSeparator()
        video_menu.addAction(video_route_action_change)
        video_menu.addAction(video_route_action)
        video_menu.addSeparator()
        video_menu.addAction(video_wvh)
        video_menu.addAction(video_cj)
        video_menu.addAction(video_xz)
        video_menu.addAction(video_fz)

        open_action.triggered.connect(self.open_file)
        close_action.triggered.connect(sys.exit)

        # 音频
        audio_menu = menu_bar.addMenu("音频")
        # 操作栏目
        open_voice_panel = QAction("显示音频控制面板", self)
        open_voice_panel.setShortcut("Ctrl+Shift+V")
        change_setting_changes = QAction("循环切换音频轨道", self)
        change_voice_routes = QAction("音频轨道", self)
        current_menu_vol = "音量 {} ".format(self.mediaplayer.audio_get_volume())
        self.change_voice_numbers = QAction(current_menu_vol, self)
        change_voice_numbers_add_5 = QAction("音量 + 5%", self)
        change_voice_numbers_add_5.setShortcut(Qt.Key.Key_Up)
        # change_voice_numbers_add_5.triggered.connect(self.set_volume())
        change_voice_numbers_sub_5 = QAction("音量 - 5%", self)
        change_voice_numbers_sub_5.setShortcut(Qt.Key.Key_Down)
        change_voice_numbers_0 = QAction("静音", self)
        change_voice_numbers_0.setShortcut("Ctrl+\\")
        change_voice_delay = QAction("音频延迟", self)
        change_voice_delay_add_5 = QAction("音频延迟 + 0.5 秒", self)
        change_voice_delay_add_5.setShortcut("Shift+)")
        change_voice_delay_sub_5 = QAction("音频延迟 - 0.5 秒", self)
        change_voice_delay_sub_5.setShortcut("Shift+(")
        change_voice_delay_0 = QAction("重制音频延迟", self)

        audio_menu.addAction(open_voice_panel)
        audio_menu.addSeparator()
        audio_menu.addAction(change_setting_changes)
        audio_menu.addAction(change_voice_routes)
        audio_menu.addSeparator()
        audio_menu.addAction(self.change_voice_numbers)
        audio_menu.addAction(change_voice_numbers_add_5)
        audio_menu.addAction(change_voice_numbers_sub_5)
        audio_menu.addAction(change_voice_numbers_0)
        audio_menu.addSeparator()
        audio_menu.addAction(change_voice_delay)
        audio_menu.addAction(change_voice_delay_add_5)
        audio_menu.addAction(change_voice_delay_sub_5)
        audio_menu.addAction(change_voice_delay_0)
        audio_menu.addSeparator()
        change_voice_device = audio_menu.addMenu("音频设备")
        open_action.triggered.connect(self.open_file)
        close_action.triggered.connect(sys.exit)
        self.listAudioDevices(change_voice_device)

        # 字幕
        subtitle_menu = menu_bar.addMenu("字幕")
        # 操作栏目
        open_subtitle_panel = QAction("显示字幕控制面板", self)
        change_subtitle_setting = QAction("循环切换字幕轨道", self)
        main_subtitle_setting = QAction("主字幕", self)
        sub_subtitle_setting = QAction("副字幕", self)
        load_other_subtitle_setting = QAction("加载外置字幕", self)
        make_big_subtitle = QAction("放大", self)
        make_small_subtitle = QAction("缩小", self)
        make_reset_subtitle = QAction("重置字幕缩放", self)
        subtitle_delay = QAction("字幕延迟", self)
        subtitle_delay_add = QAction("字幕延迟", self)
        subtitle_delay_sub = QAction("字幕延迟 + 0.5秒", self)
        subtitle_delay_reset = QAction("字幕延迟 - 0.5秒", self)
        subtitle_font = QAction("字体", self)
        subtitle_menu.addAction(open_subtitle_panel)
        subtitle_menu.addSeparator()
        subtitle_menu.addAction(change_subtitle_setting)
        subtitle_menu.addAction(main_subtitle_setting)
        subtitle_menu.addAction(sub_subtitle_setting)
        subtitle_menu.addAction(load_other_subtitle_setting)
        subtitle_menu.addSeparator()
        subtitle_menu.addAction(make_big_subtitle)
        subtitle_menu.addAction(make_small_subtitle)
        subtitle_menu.addAction(make_reset_subtitle)
        subtitle_menu.addSeparator()
        subtitle_menu.addAction(subtitle_delay)
        subtitle_menu.addAction(subtitle_delay_add)
        subtitle_menu.addAction(subtitle_delay_sub)
        subtitle_menu.addAction(subtitle_delay_reset)
        subtitle_menu.addSeparator()
        subtitle_menu.addAction(subtitle_font)


        open_action.triggered.connect(self.open_file)
        close_action.triggered.connect(sys.exit)

        # 窗口
        window_menu = menu_bar.addMenu("窗口")
        # 操作栏目
        max_action = QAction("最大", self)
        min_action = QAction("最小", self)
        normal_action = QAction("原始尺寸", self)
        min_action.setShortcut("Ctrl+M")
        full_action = QAction("全屏", self)
        min_action.setShortcut("Shift+M")
        lock_action = QAction("锁定窗口", self)
        lock_action.triggered.connect(self.lock_windows)
        lock_action.setShortcut("Ctrl+L")
        window_menu.addAction(max_action)
        window_menu.addAction(min_action)
        window_menu.addAction(full_action)
        window_menu.addAction(normal_action)
        window_menu.addSeparator()
        window_menu.addAction(lock_action)
        max_action.triggered.connect(self.showMaximized)
        min_action.triggered.connect(self.showMinimized)
        full_action.triggered.connect(self.showFullScreen)
        normal_action.triggered.connect(self.setDefaultSize)

        # 帮助
        help_menu = menu_bar.addMenu("帮助")
        # 操作栏目
        help_action = QAction("帮助", self)
        help_action.setShortcut("Ctrl+i")

        feedback_action = QAction("反馈", self)
        website_action = QAction("网站", self)
        about_action = QAction("关于", self)
        help_menu.addAction(help_action)
        help_menu.addAction(feedback_action)
        help_menu.addAction(website_action)
        help_menu.addAction(about_action)
        help_action.triggered.connect(lambda:self.openUrlByDefault('https://www.baidu.com'))
        feedback_action.triggered.connect(lambda:self.openUrlByDefault('https://www.baidu.com'))
        website_action.triggered.connect(lambda:self.openUrlByDefault('https://www.baidu.com'))
        about_action.triggered.connect(lambda:self.openUrlByDefault('https://www.baidu.com'))

    def listAudioDevices(self, menu):
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if device['max_output_channels'] > 0:
                action = QAction(f"{i}: {device['name']}", self)
                action.triggered.connect(lambda checked, dev_id=i: self.switchAudioDevice(dev_id))
                menu.addAction(action)


    def switchAudioDevice(self, device_id):
        try:
            # 获取设备名称
            device_name = sd.query_devices(device_id)['name']

            # 切换VLC音频输出设备
            audio_output_devices = self.mediaplayer.audio_output_device_enum()
            if audio_output_devices:
                for dev in audio_output_devices:
                    if device_name in dev.device:
                        self.mediaplayer.audio_output_device_set(None, dev.device)
                        print(f"Switched to device {device_id}: {device_name}")
                        break
                vlc.libvlc_audio_output_device_list_release(audio_output_devices)
        except Exception as e:
            print(f"Failed to switch to device {device_id}: {str(e)}")
    def openUrlByDefault(self,url):
        QDesktopServices.openUrl(QUrl(url))
    def setDefaultSize(self):
        self.resize(640, 400)
        self.move(int(self.width() - 640 / 2), int(self.height() - 400 / 2))

    def openShortcutFloder(self):
        download_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
        QDesktopServices.openUrl(QUrl.fromLocalFile(download_directory))

    # 播放列表面板
    def buildPlayerListTabPanel(self):
        self.playlistPanel = QWidget(self)
        self.playlistPanel.setFixedWidth(0)
        self.playlistPanel.setFixedHeight(self.height())
        self.playlistPanel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.playlistPanel.setStyleSheet("background-color: rgba(255, 255, 0,0.3);border-radius: 4px;")
        self.playlistPanel.raise_()
        self.playlistPanel.move(self.width() - 200, 0)

    # 设置面板
    def buildTabPanel(self):
        self.tabPanel = QWidget(self)
        self.tabPanel.setFixedWidth(0)
        self.tabPanel.setFixedHeight(self.height())
        self.tabPanel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.tabPanel.setStyleSheet("background-color: rgba(255, 255, 0,1);border-radius: 4px;")
        self.tabPanel.move(self.width() - 200, 0)

    # toast面板
    def buildToastPanel(self):
        self.stateToast = QLabel(self)
        self.stateToast.setFixedSize(0, 0)
        self.stateToast.setStyleSheet("background-color: rgba(255, 255, 255,0.3);border-radius: 4px;")
        self.stateToast.move(15, 15)
        self.stateToast.setText("已锁定")
        self.stateToast.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # 状态面板
    def buildStatePanel(self):
        self.state = QWidget(self)
        self.state.setFixedSize(260, 100)
        self.state.setStyleSheet("background-color: rgba(255, 255, 255,0.3);border-radius: 4px;")
        self.state.move(15, 15)
        stateLayout = QHBoxLayout(self.state)
        statePanelWidget = QWidget(self)
        statePanelWidget.setFixedSize(240, 100)
        statePanelWidget.setStyleSheet("background-color: rgba(255, 255, 255,0.05);border-radius: 4px;")
        stateLayout.addWidget(statePanelWidget)
        stateLayout.setSpacing(0)
        statePanelWidgetLayout = QHBoxLayout(statePanelWidget)
        statePanelWidgetStateIcon = QLabel()
        statePanelWidgetStateIcon.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        statePanelWidgetStateIcon.setFixedWidth(70)
        self.stateIcon = QPixmap(os.path.join(get_assets_path(), 'icons/play.png')).scaled(QSize(60, 60))
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
            "font-size:13px;color:#cccccc;background-color:transparent;")

        # stateLayout.setContentsMargins(10, 0, 0, 0)
        stateLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.state.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.state.setFixedHeight(120)

    # 控制器面板
    def buildControlPanel(self):
        # 进度条
        self.h_position_box = QHBoxLayout()
        self.timerPosition = QLabel()
        self.timerPosition.setText("00:00:00")
        self.timerPosition.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timerPosition.setStyleSheet("background-color: transparent;color:white;")
        self.timerPosition.setFixedSize(70, 20)
        self.h_position_box.addWidget(self.timerPosition)

        self.positionslider = QSlider(Qt.Orientation.Horizontal, self)
        self.positionslider.setToolTip("位置")
        self.positionslider.setMaximum(1000)
        self.positionslider.sliderMoved.connect(self.set_position)
        self.positionslider.setStyleSheet("background-color: transparent;color:white;height:18px")
        self.positionslider.setObjectName("positionSlider")

        self.h_position_box.addWidget(self.positionslider)
        self.timerTotal = QLabel()
        self.timerTotal.setStyleSheet("background-color: transparent;color:white;")
        self.timerTotal.setFixedSize(70, 20)
        self.timerTotal.setText("00:00:00")
        self.timerTotal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h_position_box.addWidget(self.timerTotal)
        self.h_position_box.setContentsMargins(0, 0, 0, 10)

        # 控制器
        # 播放按钮
        self.hbuttonbox = QHBoxLayout()
        self.playbutton = QPushButton()

        # 音量控制
        volumesliderLayout = QHBoxLayout()
        next_icon = QPixmap(os.path.join(get_assets_path(), 'icons/volume-up.png')).scaled(20, 20)
        volumesliderIcon = QIcon(next_icon)
        self.vilumesButton = QPushButton()
        self.vilumesButton.setIcon(volumesliderIcon)
        self.vilumesButton.setIconSize(QSize(20, 20))
        self.vilumesButton.setStyleSheet("background-color: transparent")
        self.vilumesButton.clicked.connect(self.toggleVolumeSet)

        self.volumeslider = QSlider(Qt.Orientation.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("音量")
        volumesliderLayout.addWidget(self.vilumesButton)
        volumesliderLayout.addWidget(self.volumeslider)
        self.hbuttonbox.addLayout(volumesliderLayout)
        self.volumeslider.valueChanged.connect(self.set_volume)
        self.volumeslider.setStyleSheet("QSlider {background-color: transparent;}")
        self.hbuttonbox.setContentsMargins(0, 0, 0, 0)
        self.hbuttonbox.setSpacing(0)
        self.hbuttonbox.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.hbuttonbox.addStretch(1)

        # 上一个按钮
        self.prevbutton = QPushButton()
        prevPlayIcon = QPixmap(os.path.join(get_assets_path(), 'icons/arr.png'))
        qtransform = QTransform()
        rotated_pixmap = prevPlayIcon.transformed(qtransform.rotate(180),
                                                  Qt.TransformationMode.SmoothTransformation).scaled(30, 30)
        self.prevbutton.setIcon(rotated_pixmap)
        self.prevbutton.setIconSize(QSize(30, 30))
        self.prevbutton.setToolTip("上一个")
        self.hbuttonbox.addWidget(self.prevbutton)
        self.prevbutton.clicked.connect(self.stop)
        self.prevbutton.setStyleSheet("QPushButton {background-color: transparent;}")
        self.prevbutton.setFixedSize(40, 40)
        # 播放按钮
        mediaPlayerIcon = QPixmap(os.path.join(get_assets_path(), 'icons/play.png'));
        self.playbutton.setIcon(mediaPlayerIcon.scaled(36, 36, Qt.AspectRatioMode.IgnoreAspectRatio,
                                                       Qt.TransformationMode.SmoothTransformation))
        self.playbutton.setIconSize(QSize(36, 36))
        self.hbuttonbox.addWidget(self.playbutton)
        self.playbutton.clicked.connect(self.play_pause)
        self.playbutton.setStyleSheet("QPushButton {background-color: transparent;}")
        self.playbutton.setFixedSize(40, 40)
        self.playbutton.setToolTip("暂停")
        # 停止按钮
        # self.stopbutton = QPushButton()
        # self.stopbutton.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/stop.png'))))
        # self.hbuttonbox.addWidget(self.stopbutton)
        # self.stopbutton.clicked.connect(self.stop)
        # self.stopbutton.setStyleSheet("QPushButton {background-color: #A3C1DA; color: red;}")
        # 下一个按钮
        self.nextbutton = QPushButton()
        next_icon = QPixmap(os.path.join(get_assets_path(), 'icons/arr.png')).scaled(28, 28)
        self.nextbutton.setIcon(next_icon)
        self.nextbutton.setIconSize(QSize(30, 30))
        self.hbuttonbox.addWidget(self.nextbutton)
        self.nextbutton.clicked.connect(self.stop)
        self.nextbutton.setStyleSheet("QPushButton {background-color: transparent;}")
        self.nextbutton.setFixedSize(40, 40)
        self.nextbutton.setToolTip("下一个")

        # lock按钮
        self.lockbutton = QPushButton()
        self.lockbutton.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/unlock.png'))))
        self.lockbutton.clicked.connect(self.lock_windows)
        self.lockbutton.setStyleSheet("QPushButton {background-color: transparent;}")
        self.lockbutton.setToolTip("置顶窗口")

        # 播放列表按钮
        self.playlistbutton = QPushButton()
        self.playlistbutton.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/menu.png'))))
        self.playlistbutton.clicked.connect(self.show_play_panel)
        self.playlistbutton.setStyleSheet("QPushButton {background-color: transparent;}")
        self.playlistbutton.setToolTip("播放列表")

        # 设置按钮
        self.settingbutton = QPushButton()
        self.settingbutton.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/settings.png'))))
        self.settingbutton.setToolTip("设置")
        self.settingbutton.clicked.connect(self.show_setting_panel)
        self.settingbutton.setStyleSheet("QPushButton {background-color: transparent;}")

        self.hsettinglayout = QHBoxLayout()
        self.hsettinglayout.addWidget(self.lockbutton)
        self.hsettinglayout.addWidget(self.playlistbutton)
        self.hsettinglayout.addWidget(self.settingbutton)

        self.hbuttonbox.addStretch(1)
        self.hbuttonbox.addLayout(self.hsettinglayout)

        self.controller = QWidget(self)
        self.controller.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.controller.setFixedHeight(78)
        self.controller.setContentsMargins(0, 5, 0, 0)
        self.controller.move(0, 200)
        self.controller_layout = QVBoxLayout()
        self.controller.setLayout(self.controller_layout)
        self.controller_layout.addLayout(self.hbuttonbox)
        self.controller_layout.addLayout(self.h_position_box)
        self.controller_layout.setSpacing(0)
        self.controller_layout.setContentsMargins(10, 0, 10, 0)
        self.controller.setStyleSheet("background-color: #ffffff;")
        self.widget.setLayout(self.v_box_layout)
        self.widget.setStyleSheet("background-color: black;")
        self.controller.setStyleSheet("background-color: rgba(255,255,255,0.2);border-radius: 4px;")
        self.controller.setStyleSheet(load_stylesheet("assets/styles/player.qss"))
        self.controller.setObjectName("controller_panel")
        self.controller.move(int((self.width() - 600) / 2), self.height() - 120)
        self.controller.setFixedSize(600, 100)

    # UI 构建
    def create_ui(self):
        self.resize(640, 400)
        self.widget = QWidget(self)
        self.buildToastPanel()
        self.buildPlayerListTabPanel()
        self.buildTabPanel()
        self.buildMenu()
        self.buildControlPanel()

        # 核心组件
        self.setCentralWidget(self.widget)
        self.widget.setStyleSheet(load_stylesheet("assets/styles/player.qss"))

        # 视频容器
        self.video_frame = QFrame()

        self.palette = self.video_frame.palette()
        self.palette.setColor(QPalette.ColorRole.Window, QColor(255, 0, 0))
        self.video_frame.setPalette(self.palette)
        self.video_frame.setAutoFillBackground(True)

        # 整体
        self.v_box_layout = QVBoxLayout()
        self.v_box_layout.addWidget(self.video_frame)
        self.v_box_layout.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.v_box_layout)

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)

        self.volumeslider.setValue(50)
        self.mediaplayer.audio_set_volume(50)

    def show_setting_panel(self):
        print(self.tabPanel.width())
        if self.tabPanel.width() <= 0:
            self.tabPanel.setFixedWidth(200)
        else:
            self.tabPanel.setFixedWidth(0)

    def show_play_panel(self):
        if self.playlistPanel.width() <= 0:
            self.playlistPanel.setFixedWidth(200)
        else:
            self.playlistPanel.setFixedWidth(0)

    def play_pause(self):
        self.playlistPanel.setFixedWidth(0)
        self.tabPanel.setFixedWidth(0)
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/pause.png'))))
            self.playbutton.setToolTip("播放")
            self.is_paused = True
            self.timer.stop()
        else:
            if self.mediaplayer.play() == -1:
                self.open_file()
                return
            self.mediaplayer.play()
            self.playbutton.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/play.png'))))
            self.playbutton.setToolTip("暂停")
            self.timer.start()
            self.is_paused = False

    def stop(self):
        self.mediaplayer.stop()
        self.playbutton.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/play.png'))))

    def set_video_rate(self, rate):
        print(rate)
        self.mediaplayer.set_rate(rate)

    def open_url_window(self):
        self.url_win = OpenUrlWindow()
        self.url_win.open_url_signal.connect(self.openUrlVideo)
        self.url_win.show()

    def open_file(self):
        dialog_txt = "选择媒体"
        filename, _ = QFileDialog.getOpenFileName(self, dialog_txt, os.path.expanduser('~'))
        if not filename:
            return

        self.media = self.instance.media_new(filename)
        self.mediaplayer.set_media(self.media)
        self.media.parse()
        self.setWindowTitle(self.media.get_meta(vlc.Meta.Title))

        sys_platform = platform.platform().lower()
        if "windows" in sys_platform:
            self.mediaplayer.set_hwnd(int(self.video_frame.winId()))
        elif "macos" in sys_platform:
            self.mediaplayer.set_nsobject(int(self.video_frame.winId()))
        elif "linux" in sys_platform:
            self.mediaplayer.set_xwindow(int(self.video_frame.winId()))
        else:
            print("其他系统")
        self.timerTotal.setText(str(convert_milliseconds_to_time(self.media.get_duration())))
        self.play_pause()
    def openUrlVideo(self,url):
        self.media = self.instance.media_new(urllib.parse.quote(url, safe=':/'))

        self.mediaplayer.set_media(self.media)
        self.media.parse()
        self.setWindowTitle(self.media.get_meta(vlc.Meta.Title))
        sys_platform = platform.platform().lower()
        if "windows" in sys_platform:
            self.mediaplayer.set_hwnd(int(self.video_frame.winId()))
        elif "macos" in sys_platform:
            self.mediaplayer.set_nsobject(int(self.video_frame.winId()))
        elif "linux" in sys_platform:
            self.mediaplayer.set_xwindow(int(self.video_frame.winId()))
        else:
            print("其他系统")
        self.timerTotal.setText(str(convert_milliseconds_to_time(self.media.get_duration())))
        self.play_pause()
    def toggleVolumeSet(self):
        if self.mediaplayer.audio_get_volume() != 0:
            self.set_volume(0)
            self.volumeslider.setValue(0)
        else:
            self.set_volume(50)
            self.volumeslider.setValue(50)


    def set_volume(self, volume):
        if volume == 0:
            next_icon = QPixmap(os.path.join(get_assets_path(), 'icons/volume-off.png')).scaled(20, 20)
            volumesliderIcon = QIcon(next_icon)
            self.vilumesButton.setIcon(volumesliderIcon)
        else:
            next_icon = QPixmap(os.path.join(get_assets_path(), 'icons/volume-up.png')).scaled(20, 20)
            volumesliderIcon = QIcon(next_icon)
            self.vilumesButton.setIcon(volumesliderIcon)
        current_menu_vol = "音量 {} ".format(volume)
        self.change_voice_numbers = QAction(current_menu_vol, self)
        self.mediaplayer.audio_set_volume(volume)

    def set_position(self, position):
        pos = position / 1000.0
        self.mediaplayer.set_position(pos)

    def update_ui(self):
        media_pos = int(self.mediaplayer.get_position() * 1000)
        self.positionslider.setValue(media_pos)
        self.timerPosition.setText(str(convert_milliseconds_to_time(self.mediaplayer.get_time())))
        if not self.mediaplayer.is_playing():
            self.timer.stop()
            if not self.is_paused:
                self.stop()

    def lock_windows(self):
        flags = self.windowFlags()
        if flags & Qt.WindowType.WindowStaysOnTopHint:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
            self.lockbutton.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/unlock.png'))))
            self.lockbutton.setToolTip("窗口已置顶")
            self.show()
            self.stateToast.setFixedSize(0, 0)
        else:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
            self.lockbutton.setIcon(QIcon(QPixmap(os.path.join(get_assets_path(), 'icons/lock.png'))))
            self.lockbutton.setToolTip("置顶窗口")
            self.show()
            self.stateToast.setFixedSize(100, 30)

    def resizeEvent(self, event):
        if self.tabPanel != None:
            self.tabPanel.move(self.width() - 200, 0)
            self.tabPanel.setFixedHeight(self.height())
        if self.controller != None:
            self.controller.move(int((self.width() - 600) / 2), self.height() - 120)
            self.controller.setFixedSize(600, 100)
        if self.playlistPanel != None:
            self.playlistPanel.move(self.width() - 200, 0)
            self.playlistPanel.setFixedHeight(self.height())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.window_pos = self.frameGeometry().topLeft()
            self.start_pos = event.globalPosition().toPoint()
            self.is_mouse_pressed = True

    def mouseMoveEvent(self, event):
        if self.is_mouse_pressed:
            self.mouse_has_moved = True
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
            delta = event.globalPosition().toPoint() - self.start_pos
            self.move(self.pos() + delta)
            self.start_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.end_pos = event.globalPosition()
            self.play_pause()
            self.start_pos = None
            self.end_pos = None
            self.mouse_has_moved = None
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))


def main():
    app = QApplication(sys.argv)
    player = MediaPlayer()
    player.show()
    player.resize(640, 400)
    sys.exit(app.exec())


class OpenUrlWindow(QDialog):
    open_url_signal = Signal(str)  #

    def __init__(self):
        super().__init__()
        self.setWindowTitle('打开URL...')
        self.setFixedSize(500, 110)
        self.setStyleSheet("background-color: rgba(255, 255, 255,0);")
        # 其他
        self.mainWidget = QWidget(self)
        self.open_url_layout = QVBoxLayout()
        self.open_url_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.open_url_layout.setContentsMargins(10, 10, 10, 10)
        self.open_url_layout.setSpacing(10)
        self.mainWidget.setLayout(self.open_url_layout)

        self.input_url = QLineEdit(self)
        self.input_url.setFixedHeight(50)
        self.input_url.setStyleSheet("padding-left: 10px;font-size: 24px;color:grey;")
        self.input_url.setPlaceholderText("在此输入URL ...")

        self.open_url_layout.addWidget(self.input_url)

        self.cancel_button = QPushButton(self)
        self.confirm_button = QPushButton(self)
        self.cancel_button.setText("取消")
        self.cancel_button.setFixedSize(80,30)
        self.confirm_button.setText("打开")
        self.cancel_button.clicked.connect(self.close)
        self.confirm_button.clicked.connect(self.openUrl) #打开操作 todo
        self.confirm_button.setFixedSize(80, 30)

        self.actions_layout = QHBoxLayout()
        self.actions_layout.addWidget(self.cancel_button)
        self.actions_layout.addWidget(self.confirm_button)
        self.actions_layout.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.open_url_layout.addLayout(self.actions_layout)

        self.mainWidget.resize(500, 110)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        radius = 4
        self.mainWidget.setStyleSheet(
            """
            background:rgba(200, 200, 200,0.9);
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(255, 255, 255, 160))
        shadow_effect.setOffset(5, 5)
        self.mainWidget.setGraphicsEffect(shadow_effect)

    def openUrl(self):
        self.open_url_signal.emit(self.input_url.text())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.window_pos = self.frameGeometry().topLeft()
            self.start_pos = event.globalPosition().toPoint()
            self.is_mouse_pressed = True

    def mouseMoveEvent(self, event):
        if self.is_mouse_pressed:
            self.mouse_has_moved = True
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
            delta = event.globalPosition().toPoint() - self.start_pos
            self.move(self.pos() + delta)
            self.start_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.end_pos = event.globalPosition()
            self.start_pos = None
            self.end_pos = None
            self.mouse_has_moved = None
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))


if __name__ == "__main__":
    main()
