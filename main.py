import sys
from PyQt5.QtWidgets import QApplication

from note import Note

# 主函數，運行應用程式
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Note()
    window.show()
    sys.exit(app.exec_())