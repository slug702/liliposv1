from PySide6.QtCore import QSize, Qt, QRunnable, QThreadPool, Signal, QObject, Slot
from PySide6.QtGui import QAction, QIcon, QPalette, QColor, QPixmap, QFontDatabase
from PySide6.QtCore import QSize, Qt, QRunnable, QThreadPool, Signal, QTimer
from PySide6.QtGui import QAction, QIcon, QPalette, QColor, QPixmap, QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (QMainWindow, QToolBar, QPushButton, QStatusBar, QGridLayout, QLabel,
                               QWidget, QComboBox, QLineEdit, QSpacerItem, QSizePolicy, QApplication, QMessageBox, QDialog, QVBoxLayout, QProgressBar)
from datetime import datetime
from databaseutils import DatabaseManager
from saleslandingpage import POSHomePage


class MainLoginWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #f0f4ff;")  # Soft bluish background
        self.setWindowTitle("lili's point-of-sale")
        self.resize(600, 700)
        self.database_manager = DatabaseManager()
        login_screenLayout = QGridLayout()
        login_screenLayout.setContentsMargins(50, 60, 50, 60)

        # ---- Branding Header ----
        branding_widget = QWidget()
        branding_layout = QVBoxLayout(branding_widget)
        branding_layout.setContentsMargins(0, 0, 0, 0)
        branding_layout.setSpacing(4)

        logo = QLabel()
        logo_pixmap = QPixmap('_internal/resources/images/lilslogin.png')
        logo.setPixmap(logo_pixmap.scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        branding_layout.addWidget(logo)

        shop_name = QLabel("lili systems")
        shop_name.setStyleSheet("font-size: 50px; font-weight: bold; color: #003566; letter-spacing: 2px; font-family: 'Segoe UI', sans-serif;")
        shop_name.setAlignment(Qt.AlignCenter)
        branding_layout.addWidget(shop_name)

        # Updated sub-brand text
        orpadi_note = QLabel("by ORPADI Corp.")
        orpadi_note.setStyleSheet("font-size: 20px; color: #0077b6; font-family: 'Segoe UI', sans-serif;")
        orpadi_note.setAlignment(Qt.AlignCenter)
        branding_layout.addWidget(orpadi_note)

        branding_layout.addSpacing(14)
        login_screenLayout.addWidget(branding_widget, 0, 0, 1, 3, Qt.AlignTop)

        # ---- Login Form Card ----
        login_card = QWidget()
        login_card_layout = QVBoxLayout(login_card)
        login_card_layout.setContentsMargins(30, 30, 30, 30)
        login_card.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border-radius: 22px;
                border: 2px solid #b0c4de;
                box-shadow: 0 4px 24px rgba(0, 119, 182, 0.08);
            }
        """)

        self.selectuserbox = QComboBox()
        self.selectuserbox.setStyleSheet("""
            QComboBox {
                font-size: 17px;
                font-family: 'Segoe UI', sans-serif;
                color: #003566;
                background-color: #eaf4ff;
                border: 2px solid #89c2d9;
                border-radius: 12px;
                padding: 9px 16px;
                min-width: 12em;
                margin-bottom: 4px;
            }
            QComboBox::drop-down {
                width: 0px;
                border: none;
                background: none;
            }
            QComboBox::down-arrow {
                width: 0px;
                height: 0px;
            }
            QComboBox:focus {
                border: 2px solid #0077b6;
            }
            QComboBox QAbstractItemView {
                background: #ffffff;
                font-size: 18px;
            }
        """)
        login_card_layout.addWidget(self.selectuserbox)

        self.passwordbox = QLineEdit(placeholderText="Enter Password")
        self.passwordbox.setEchoMode(QLineEdit.Password)
        self.passwordbox.setStyleSheet("""
            QLineEdit {
                font-size: 17px;
                font-family: 'Segoe UI', sans-serif;
                color: #003566;
                background-color: #eaf4ff;
                border-radius: 12px;
                border: 2px solid #89c2d9;
                padding: 9px 16px;
                margin-bottom: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #0077b6;
            }
        """)
        login_card_layout.addWidget(self.passwordbox)

        self.login_mainbtn = QPushButton("Login")
        self.login_mainbtn.setStyleSheet("""
            QPushButton {
                background-color: #0077b6;
                color: #fff;
                border: none;
                border-radius: 10px;
                font-size: 17px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: 600;
                padding: 11px 0;
                margin-top: 20px;
                box-shadow: 0 2px 12px rgba(0, 119, 182, 0.2);
            }
            QPushButton:hover {
                background-color: #023e8a;
                color: #fff;
            }
        """)
        self.login_mainbtn.setIconSize(QSize(24, 24))
        self.login_mainbtn.clicked.connect(self.login_Clicked)
        login_card_layout.addWidget(self.login_mainbtn)

        login_hint = QLabel("IT Department: 09171550252 (Globe) or 09218614475 (Smart)")
        login_hint.setStyleSheet("color:#7ca1c2; font-size: 13px; margin-top: 5px; font-family: 'Segoe UI',sans-serif;")
        login_hint.setAlignment(Qt.AlignCenter)
        login_card_layout.addWidget(login_hint)

        login_screenLayout.addWidget(login_card, 1, 0, 1, 3, Qt.AlignVCenter)
        self.setLayout(login_screenLayout)
        self.center_window()
        self.populate_usernames()
    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    def populate_usernames(self):
        usernames = self.database_manager.fetch_usernames()
        self.selectuserbox.addItems(usernames)
    def login_Clicked(self):
        username = self.selectuserbox.currentText()
        password = self.passwordbox.text()
        rank = self.database_manager.get_passlevel(username)
        if self.database_manager.verify_credentials(username, password):

            self.next_screenacc = POSHomePage(username, rank)
            self.next_screenacc.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Login Error", "Incorrect username or password")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainLoginWindow()
    window.show()
    sys.exit(app.exec_()) 
            
 