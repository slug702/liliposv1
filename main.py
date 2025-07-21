from PySide6.QtWidgets import QApplication 
from loginpage import MainLoginWindow

import sys  

app = QApplication(sys.argv)
window = MainLoginWindow()

window.show() 
app.exec()
