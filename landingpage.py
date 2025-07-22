from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout

class POSHomePage(QWidget):
    def __init__(self, username, rank, parent=None):
        super().__init__(parent)
        self.setWindowTitle("POS Home - Lili's Systems")
        self.username = username
        self.setMinimumSize(900, 600)

        # Header
        self.header = QLabel(f"Welcome, {username}! Position: {rank}")
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

        # Navigation buttons
        self.btn_sales = QPushButton("Sales")
        self.btn_inventory = QPushButton("Inventory")
        self.btn_reports = QPushButton("Reports")
        self.btn_settings = QPushButton("Settings")
        for btn in [self.btn_sales, self.btn_inventory, self.btn_reports, self.btn_settings]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet("font-size: 18px;")

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
        self.main_area = QLabel("Select a section above to begin.")
        self.main_area.setStyleSheet("font-size: 20px; color: gray; margin-top: 40px;")

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.header)
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.main_area)

    # Example methods to show how you’d swap widgets
    def show_sales(self):
        self.main_area.setText("Sales interface goes here (you can swap in a QWidget here).")
    def show_inventory(self):
        self.main_area.setText("Inventory management UI goes here.")
    def show_reports(self):
        self.main_area.setText("Reports section UI goes here.")
    def show_settings(self):
        self.main_area.setText("Settings page UI goes here.")

# Usage (after login success):
# self.next_screenacc = POSHomePage(username)
# self.next_screenacc.show()
# self.hide()
