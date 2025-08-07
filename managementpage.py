from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QApplication, QTableWidget, QSizePolicy, QHeaderView, QTableView, QTableWidgetItem

class ManagementPage(QWidget):
    def __init__(self, username, rank, parent=None):
        super().__init__(parent)
        self.setWindowTitle("POS Home - Lili's Systems")
        self.username = username
        self.showMaximized()
        #self.center_window()
        # Header
        self.header = QLabel(f"Today's Order List")
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; font-family: 'Segoe UI', sans-serif")
        
        # Navigation buttons
        self.btn_sales = QPushButton("Sales")
        self.btn_inventory = QPushButton("Inventory")
        self.btn_reports = QPushButton("Reports")
        self.btn_settings = QPushButton("Settings")
        for btn in [self.btn_sales, self.btn_inventory, self.btn_reports, self.btn_settings]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet("font-size: 18px; font-family: 'Segoe UI', sans-serif")
        
        

      
        # Main area (will swap out widgets here)
        #self.main_area = QLabel("Select a section above to begin.")
        #self.main_area.setStyleSheet("font-size: 20px; color: gray; margin-top: 40px; font-family: 'Segoe UI', sans-serif")

        main_layout = QVBoxLayout(self)
        header_layout = QHBoxLayout(self)
        # === ORDER SUMMARY CART ===
        table_layout = QHBoxLayout(self)
        self.order_table = QTableWidget(5, 3)
        self.order_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.order_table.setHorizontalHeaderLabels(["quantity", "product", "price"])
        self.order_table.verticalHeader().setVisible(False)
        self.order_table.setSelectionBehavior(QTableView.SelectRows)
        self.order_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.order_table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                border: 2px solid #D1D5DB;  /* Light border */
                border-radius: 16px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 15px;
                font-weight: 500;
                color: #1F2937;
                gridline-color: transparent;
                padding: 4px;
            }

            QHeaderView::section {
                background-color: #F3F4F6;
                color: #111827;
                font-size: 15px;
                font-weight: bold;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #D1D5DB;
            }

            QTableWidget::item {
                padding: 10px;
                border: none;
            }

            QTableCornerButton::section {
                background-color: #F3F4F6;
                border: none;
            }

            QScrollBar:vertical {
                border: none;
                background: #E5E7EB;
                width: 14px;
                margin: 20px 0;
                border-radius: 7px;
            }

            QScrollBar::handle:vertical {
                background: #9CA3AF;
                min-height: 20px;
                border-radius: 7px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
        """)

        self.button_style = """
            QPushButton {
                background-color: #0077b6;  /* Deep navy blue */
                color: white;
                border-radius: 20px;  /* More rounded */
                padding: 10px 24px;
                font-size: 15px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: 500; 
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #023e8a;
            }
            QPushButton:pressed {
                background-color: #023e8a;
            }
            QPushButton:disabled {
                background-color: #cbd5e0;
                color: #ffffff;
            }
        """


        order_data = [["3", "meal3", "3"], ["3", "fried chicken", "3"], ["3", "burger", "3"]]
        for i, row in enumerate(order_data):
            for j, val in enumerate(row):
                self.order_table.setItem(i, j, QTableWidgetItem(val))
        self.edit_products = QPushButton("Edit Products")
        header_layout.addWidget(self.edit_products)
        main_layout.addLayout(header_layout)
        main_layout.addLayout(table_layout)
        nav_layout = QVBoxLayout()
        table_layout.addLayout(nav_layout)
        
        self.gotoorders = QPushButton ("Orders")
        self.gotoinventory = QPushButton ("Inventory")
        self.gotosettings = QPushButton ("Setting")
        self.gotoreports = QPushButton ("Report")
        self.gotomanagement = QPushButton ("Management")
        nav_layout.addWidget(self.gotoorders)
        nav_layout.addWidget(self.gotoinventory)
        nav_layout.addWidget(self.gotosettings)
        nav_layout.addWidget(self.gotoreports)
        nav_layout.addWidget(self.gotomanagement)
        
        #main_layout.addLayout(nav_layout)
        table_layout.addWidget(self.order_table)
        for btn in [self.gotoorders, self.gotoinventory, self.gotosettings, self.gotoreports, self.gotomanagement, self.edit_products]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet(self.button_style)    
        
        

    # Example methods to show how you’d swap widgets
    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    


