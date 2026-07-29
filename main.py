from PySide6.QtWidgets import QApplication
from ui import MainWindow

app = QApplication([])

window = MainWindow()

window.show()

app.exec()
