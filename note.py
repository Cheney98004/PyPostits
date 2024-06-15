import sys
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QPushButton, QTextEdit, QCheckBox, QMessageBox
from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
import configparser

class Note(QWidget):
    def __init__(self):
        super().__init__()
        self.offset = None
        self.title = "PyPostits"
        
        # 定義可選的顏色主題
        self.colours = [["#FFF68F", "#FFFACD", "#CDC673"], ["#FF9CCD", "#FFC4CD", "#B26E90"]]
        self.colour_item = 0
        self.colour = self.colours[self.colour_item]
        
        # 設置窗口大小和屬性
        self.resize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SplashScreen | Qt.WindowStaysOnTopHint)
        
        # 創建頂部框架
        self.top_frame = QFrame(self)
        self.top_frame.setGeometry(0, 0, 400, 40)
        self.top_frame.setStyleSheet(f"background-color: {self.colour[0]}")

        # 創建標題標籤
        self.title_label = QLabel(self.top_frame)
        self.title_label.setText(self.title)
        self.title_label.setGeometry(15, 1, 90, 40)
        self.title_label.setStyleSheet("font: normal normal 20px \"Arial\";")

        # 創建完成勾選框
        self.check_done = QCheckBox(self.top_frame)
        self.check_done.setText("Done")
        self.check_done.setGeometry(120, 3, 60, 40)
        self.check_done.setChecked(False)

        # 創建菜單按鈕
        self.menu_button = QPushButton(self.top_frame)
        self.menu_button.setIcon(QIcon("images/menu.png"))
        self.menu_button.setGeometry(320, 0, 40, 40)
        self.menu_button.setStyleSheet("""
            QPushButton {background: %s;border: none;} QPushButton:hover {background: %s;}
        """ % (self.colour[0], self.colour[2]))
        self.menu_button.clicked.connect(self.menu_event)

        # 創建關閉按鈕
        self.close_button = QPushButton(self.top_frame)
        self.close_button.setIcon(QIcon("images/close.png"))
        self.close_button.setGeometry(360, 0, 40, 40)
        self.close_button.setStyleSheet("""
            QPushButton {background: %s;border: none;} QPushButton:hover {background: %s;}
        """ % (self.colour[0], self.colour[2]))
        self.close_button.clicked.connect(self.close_event)

        # 創建文本編輯區域
        self.textedit = QTextEdit(self)
        self.textedit.setGeometry(0, 40, 400, 260)
        self.textedit.setStyleSheet(f"background-color: {self.colour[1]};font-size: 24px;border: none;")

        # 嘗試加載設置，如果失敗則跳過
        try:
            self.load_setting()
            self.reset_colour()
        except:
            pass

    # 監聽鼠標按下事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
    
    # 監聽鼠標移動事件
    def mouseMoveEvent(self, event):
        if self.offset is not None:
            delta = QPoint(event.pos() - self.offset)
            self.move(self.pos() + delta)
            
    # 監聽鼠標釋放事件
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = None

    # 菜單事件，顯示菜單對話框
    def menu_event(self):
        self.menu_dialog = QDialog(self)
        self.menu_dialog.setWindowTitle("PyPostits")
        self.menu_dialog.resize(400, 300)
        self.menu_dialog.setFixedSize(400, 300)

        # 菜單對話框內的標題設置
        self.mtitle_label = QLabel(self.menu_dialog)
        self.mtitle_label.setText("Title")
        self.mtitle_label.setGeometry(10, 8, 80, 40)
        self.mtitle_label.setStyleSheet("font: normal normal 24px \"Arial\"")
        self.title_lineedit = QLineEdit(self.menu_dialog)
        self.title_lineedit.setText(self.title)
        self.title_lineedit.setGeometry(90, 8, 300, 40)
        self.title_lineedit.setStyleSheet("font: normal normal 20px \"Arial\"")

        # 菜單對話框內的顏色設置
        self.colour_label = QLabel(self.menu_dialog)
        self.colour_label.setText("Colour")
        self.colour_label.setGeometry(10, 50, 80, 40)
        self.colour_label.setStyleSheet("font: normal normal 24px \"Arial\"")
        self.mcolours = ["yellow", "pink"]
        self.colour_combo = QComboBox(self.menu_dialog)
        self.colour_combo.setGeometry(90, 50, 300, 40)
        self.colour_combo.addItems(self.mcolours)
        for i in range(2):
            self.colour_combo.setItemIcon(i, QIcon(f"images/{self.mcolours[i]}.png"))

        # 應用按鈕
        apply_button = QPushButton(self.menu_dialog)
        apply_button.setText("Apply")
        apply_button.setGeometry(330, 262, 60, 30)
        apply_button.clicked.connect(self.menu_apply_event)

        # 計算並設置對話框位置
        main_window_geometry = self.geometry()
        if main_window_geometry.x() >= 500:
            dialog_x = main_window_geometry.left() - self.menu_dialog.width() - 10
            dialog_y = main_window_geometry.top()
        else:
            dialog_x = main_window_geometry.left() + self.menu_dialog.width() + 10
            dialog_y = main_window_geometry.top()
        self.menu_dialog.move(dialog_x, dialog_y)

        # 顯示對話框
        self.menu_dialog.exec()

        # 更新標題和顏色
        self.title = self.title_lineedit.text()
        self.title_label.setText(self.title)
        self.colour_item = self.colour_combo.currentIndex()
        self.reset_colour()

    # 重置顏色
    def reset_colour(self):
        self.colour = self.colours[self.colour_item]
        self.top_frame.setStyleSheet(f"background-color: {self.colour[0]}")
        self.menu_button.setStyleSheet("""
            QPushButton {background: %s;border: none;} QPushButton:hover {background: %s;}
        """ % (self.colour[0], self.colour[2]))
        self.close_button.setStyleSheet("""
            QPushButton {background: %s;border: none;} QPushButton:hover {background: %s;}
        """ % (self.colour[0], self.colour[2]))
        self.textedit.setStyleSheet(f"background-color: {self.colour[1]};font-size: 24px;border: none;")

    # 菜單應用事件，應用設置
    def menu_apply_event(self):
        self.title = self.title_lineedit.text()
        self.title_label.setText(self.title)
        self.colour_item = self.colour_combo.currentIndex()
        self.colour = self.colours[self.colour_item]
        self.reset_colour()

    # 寫入設置到文件
    def write_setting(self):
        self.file = open("notes/n1.ini", "w")
        config = configparser.ConfigParser()
        config["Basic"] = {}
        config["Basic"]["title"] = self.title
        config["Basic"]["colouritem"] = str(self.colour_item)
        config["Contents"] = {}
        config["Contents"]["text"] = self.textedit.toPlainText()
        config.write(self.file)

    # 從文件加載設置
    def load_setting(self):
        config = configparser.ConfigParser()
        config.read("notes/n1.ini")
        self.title = config["Basic"]["title"]
        self.colour_item = int(config["Basic"]["colouritem"])
        self.textedit.setText(str(config["Contents"]["text"]))

    # 關閉事件，檢查任務是否完成
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
                self.write_setting()
                sys.exit()
        else:
            self.write_setting()
            sys.exit()