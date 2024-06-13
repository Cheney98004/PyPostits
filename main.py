import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QFrame, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon

class Note(QWidget):
    def __init__(self):
        super().__init__()
        self.offset = None
        self.title = "便利貼"
        self.resize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SplashScreen | Qt.WindowStaysOnTopHint)
        
        self.top_frame = QFrame(self)
        self.top_frame.setGeometry(0, 0, 400, 40)
        self.top_frame.setStyleSheet("background-color: #FFF68F")

        self.title_label = QLabel(self.top_frame)
        self.title_label.setText(self.title)
        self.title_label.setGeometry(5, 5, 60, 30)
        self.title_label.setStyleSheet("font-size: 18px;")

        self.close_button = QPushButton(self.top_frame)
        self.close_button.setIcon(QIcon("images/close.png"))
        self.close_button.setGeometry(360, 0, 40, 40)
        self.close_button.setStyleSheet("""
            QPushButton{background: #FFF68F;border: none;} QPushButton:hover{background: #CDC673;}
        """)
        self.close_button.clicked.connect(self.close_event)

        self.textedit = QTextEdit(self)
        self.textedit.setGeometry(0, 40, 400, 260)
        self.textedit.setStyleSheet("background-color: #FFFACD;font-size: 24px;border: none;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
    
    def mouseMoveEvent(self, event):
        if self.offset is not None:
            delta = QPoint(event.pos() - self.offset)
            self.move(self.pos() + delta)
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = None

    def close_event(self):
        sys.exit()

class Main_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry()
        self.setWindowTitle("便利貼")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Note()
    window.show()
    sys.exit(app.exec_())