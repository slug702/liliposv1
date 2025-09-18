from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QApplication
from decimal import Decimal
class POSHomePage(QWidget):
    def __init__(self, username, rank, parent=None):
        super().__init__(parent)
        self.setWindowTitle("POS Home - Lili's Systems")
        self.username = username
        self.showMaximized()
        #self.center_window()
        # Header
        self.header = QLabel(f"welcome, {username}! Position: {rank}")
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; font-family: 'Segoe UI', sans-serif")
        
        # Navigation buttons
        self.btn_sales = QPushButton("Sales")
        self.btn_inventory = QPushButton("Inventory")
        self.btn_reports = QPushButton("Reports")
        self.btn_settings = QPushButton("Settings")
        for btn in [self.btn_sales, self.btn_inventory, self.btn_reports, self.btn_settings]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet("font-size: 18px; font-family: 'Segoe UI', sans-serif")
        
        # Connect buttons to placeholder slot functions
        self.btn_sales.clicked.connect(self.show_sales)
        self.btn_inventory.clicked.connect(self.show_inventory)
        self.btn_reports.clicked.connect(self.show_reports)
        self.btn_settings.clicked.connect(self.show_settings)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.btn_sales)
        nav_layout.addWidget(self.btn_inventory)
        nav_layout.addWidget(self.btn_reports)
        nav_layout.addWidget(self.btn_settings)

        # Main area (will swap out widgets here)
        #self.main_area = QLabel("Select a section above to begin.")
        #self.main_area.setStyleSheet("font-size: 20px; color: gray; margin-top: 40px; font-family: 'Segoe UI', sans-serif")

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.header)
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.main_area)
        
    # Example methods to show how you’d swap widgets
    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    def show_sales(self):
        print("go to sales")
    def show_inventory(self):
        print("go to inventory")
    def show_reports(self):
        print("go to reports")
    def show_settings(self):
        print("go to settings")


