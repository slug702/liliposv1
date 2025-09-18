from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QApplication, QTableWidget, QSizePolicy, QHeaderView, QTableView, QTableWidgetItem
from decimal import Decimal
from datetime import date

class ManagementPage(QWidget):
    def __init__(self, username, rank, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Management Page - Lili Systems")
        self.username = username
        self.rank = rank
        self.showMaximized()
        #self.center_window()
        # Header
        self.header = QLabel(f"Today's Order List")
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; font-family: 'Segoe UI', sans-serif")
        self.date_today = date.today()
    
        

      
        # Main area (will swap out widgets here)
        #self.main_area = QLabel("Select a section above to begin.")
        #self.main_area.setStyleSheet("font-size: 20px; color: gray; margin-top: 40px; font-family: 'Segoe UI', sans-serif")

        main_layout = QVBoxLayout(self)
        header_layout = QHBoxLayout(self)
        # === ORDER SUMMARY CART ===
        table_layout = QHBoxLayout(self)
        self.order_table = QTableWidget(5, 5)
        self.order_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.order_table.setHorizontalHeaderLabels(["Order Number", "Paid", "Mode of Payment", "User", "Order Type"])
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


        order_data = [["1", "1250", "Card", "Cashier 1", "Table 1"], ["2", "1000", "Cash", "Cashier 3", "Takeout"], ["3", "500", "GCash", "Cashier 4","Table 4"]]
        for i, row in enumerate(order_data):
            for j, val in enumerate(row):
                self.order_table.setItem(i, j, QTableWidgetItem(val))
        self.header_label = QLabel("Management Page")
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px")
        self.header_label2 = QLabel(f"Orders Placed as of {self.date_today}")
        self.header_label2.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px")
        header_layout.addWidget(self.header_label)
        header_layout.addWidget(self.header_label2)
        
        main_layout.addLayout(header_layout)
        main_layout.addLayout(table_layout)
        nav_layout = QVBoxLayout()
        table_layout.addLayout(nav_layout)
        
        self.gohome = QPushButton ("Go Back to Orders")
        self.gohome.clicked.connect(self.gobacktohome)
        self.deleteinv = QPushButton ("Delete Invoice")
        self.gotoproducts= QPushButton ("Product List")
        self.gotoproducts.clicked.connect(self.gotoproductlist)
        self.gotocombos = QPushButton ("Combo List - TBD")
        
        nav_layout.addWidget(self.gohome)
        nav_layout.addWidget(self.deleteinv)
        nav_layout.addWidget(self.gotoproducts)
        nav_layout.addWidget(self.gotocombos)
        
        
        #main_layout.addLayout(nav_layout)
        table_layout.addWidget(self.order_table)
        for btn in [self.gohome, self.deleteinv, self.gotoproducts, self.gotocombos]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet(self.button_style)    
    def gotoproductlist(self):
        from productlist import ProductPage
        self.next_screenproducts = ProductPage(self.username, self.rank)
        self.next_screenproducts.show()
        self.hide()
    def gobacktohome(self):
        from saleslandingpage import POSHomePage
        self.next_screenacc = POSHomePage(self.username, self.rank)
        self.next_screenacc.show()
        self.hide()

    # Example methods to show how you’d swap widgets
    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    


