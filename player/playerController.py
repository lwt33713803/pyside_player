from PySide6.QtWidgets import QWidget


class PlayerController(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setStyleSheet("background-color: rgba(0, 0, 0,0,0.4);")
        self.offset = None

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass
        # print("z组件移动了")