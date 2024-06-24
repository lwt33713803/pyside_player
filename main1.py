import sys

from PySide6.QtCore import QUrl, QDir, QFileInfo, Qt
from PySide6.QtGui import QCursor
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from start.ui_main_window import UiMainWindow as StartUI
from player.ui_main_window import UiMainWindow as PlayerUI


class MainWindow(QMainWindow, StartUI):
    def __init__(self):
        super().__init__()
        self.dialog = None
        self.setupUi(self)
        # self.registerAction()
        self.center()

    # def registerAction(self):
    #     self.openUrlWidget.clicked.connect(self.open_new_window)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class PlayerWindow(QMainWindow, PlayerUI):
    def __init__(self):
        super().__init__()
        self.mouse_has_moved = None
        self.window_pos = None
        self.setupUi(self)
        # self._audio_output = QAudioOutput()
        # self._player = QMediaPlayer()
        # self._player.setAudioOutput(self._audio_output)
        # self._player.setVideoOutput(self.playOutWidget)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openDemo(self):
        currPath = QDir.currentPath()
        title = "选择视频文件"
        file = "视频格式(*.wmv,*.mp4,*.avi,*.flv);所有文件(*.*)"
        fileName, fit = QFileDialog.getOpenFileName(self, title, currPath, file)
        if fileName == '':
            return
        fileInfo = QFileInfo(fileName)
        baseName = fileInfo.fileName()
        # self.titlebarTitle.setText(baseName)
        # media = QUrl.fromLocalFile(fileName)
        self.playOutWidget.setVideo(QUrl.fromLocalFile(fileName))
        self.playOutWidget.play()
        # self._player.setSource(media)
        # self._player.play()

    def closePlayerWindows(self):
        self.close()

    def minPlayerWindows(self):
        self.setWindowState(Qt.WindowState.WindowMinimized)

    def maxPlayerWindows(self):
        if self.isFullScreen():
            self.setWindowState(Qt.WindowState.WindowMaximized)
        else:
            self.setWindowState(Qt.WindowState.WindowFullScreen)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         self.window_pos = self.frameGeometry().topLeft()
    #         self.start_pos = event.globalPosition().toPoint()
    #         self.is_mouse_pressed = True
    #
    # def mouseMoveEvent(self, event):
    #     if self.is_mouse_pressed:
    #         self.mouse_has_moved = True
    #         self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
    #         delta = event.globalPosition().toPoint() - self.start_pos
    #         self.move(self.pos() + delta)
    #         self.start_pos = event.globalPosition().toPoint()
    #
    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         self.end_pos = event.globalPosition()
    #         if self.mouse_has_moved:
    #             print("鼠标移动过了")
    #         else:
    #             self.on_menu_press()
    #         self.start_pos = None
    #         self.end_pos = None
    #         self.mouse_has_moved = None
    #         self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def showEvent(self, event):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlayerWindow()
    window.show()
    # 设置样式表
    # apply_stylesheet(app, theme='dark_teal.xml')
    sys.exit(app.exec())
