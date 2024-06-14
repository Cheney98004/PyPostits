import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QFrame, QPushButton, QTextEdit, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon

class Note(QWidget):
    def __init__(self):
        super().__init__()
        self.offset = None
        self.title = "PyPostits"
        self.resize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SplashScreen | Qt.WindowStaysOnTopHint)
        
        self.top_frame = QFrame(self)
        self.top_frame.setGeometry(0, 0, 400, 40)
        self.top_frame.setStyleSheet("background-color: #FFF68F")

        self.title_label = QLabel(self.top_frame)
        self.title_label.setText(self.title)
        self.title_label.setGeometry(15, 3, 90, 40)
        self.title_label.setStyleSheet("font: normal normal 20px \"Arial\";")

        self.check_done = QCheckBox(self.top_frame)
        self.check_done.setText("Done")
        self.check_done.setGeometry(120, 3, 60, 40)
        self.check_done.setChecked(False)

        self.menu_button = QPushButton(self.top_frame)
        self.menu_button.setIcon(QIcon("images/menu.png"))
        self.menu_button.setGeometry(320, 0, 40, 40)
        self.menu_button.setStyleSheet("""
            QPushButton{background: #FFF68F;border: none;} QPushButton:hover{background: #CDC673;}
        """)
        self.menu_button.clicked.connect(self.menu_event)

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

    def menu_event(self):
        pass

    def close_event(self):
        if not self.check_done.isChecked():
            check_message = QMessageBox(self)
            check_message.setWindowTitle("PyPostits")
            check_message.setText("You have not completed this task.\nDo you want to close it?")
            check_message.setIcon(4)
            check_message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            check_message.setDefaultButton(QMessageBox.No)

            ret = check_message.exec()
            if ret == QMessageBox.Yes:
                sys.exit()
        else:
            sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Note()
    window.show()
    sys.exit(app.exec_())
