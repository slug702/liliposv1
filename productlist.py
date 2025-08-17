from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QApplication, QTableWidget, QSizePolicy, QHeaderView, QTableView, QTableWidgetItem
from databaseutils import DatabaseManager
from datetime import date

class ProductPage(QWidget):
    def __init__(self, username, rank, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Product List - Lili Systems")
        self.username = username
        self.rank = rank
        self.showMaximized()
        #self.center_window()
        # Header
        self.header = QLabel(f"Product List")
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; font-family: 'Segoe UI', sans-serif")
        self.date_today = date.today()
        
        
        self.db_manager = DatabaseManager()

      
        # Main area (will swap out widgets here)
        #self.main_area = QLabel("Select a section above to begin.")
        #self.main_area.setStyleSheet("font-size: 20px; color: gray; margin-top: 40px; font-family: 'Segoe UI', sans-serif")

        main_layout = QVBoxLayout(self)
        header_layout = QHBoxLayout(self)
        # === ORDER SUMMARY CART ===
        table_layout = QHBoxLayout(self)
        self.product_table = QTableWidget(7, 7)
        self.product_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.product_table.setHorizontalHeaderLabels(["Product ID", "Product", "Price", "Size", "Category", "Sub-Category", "Size Group"])
        self.product_table.verticalHeader().setVisible(False)
        self.product_table.setSelectionBehavior(QTableView.SelectRows)
        self.product_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.product_table.setStyleSheet("""
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


        self.load_products_into_table()
        self.header_label = QLabel("Product List")
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px")
        self.header_label2 = QLabel(f"TBD")
        self.header_label2.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px")
        header_layout.addWidget(self.header_label)
        header_layout.addWidget(self.header_label2)
        
        main_layout.addLayout(header_layout)
        main_layout.addLayout(table_layout)
        nav_layout = QVBoxLayout()
        table_layout.addLayout(nav_layout)
        
        
        self.gomanage = QPushButton ("Go Back to Management")
        self.gomanage.clicked.connect(self.gobacktomanagement)
        self.gohome = QPushButton ("Go Back to Orders")
        self.gohome.clicked.connect(self.gobacktohome)
        self.createprod = QPushButton ("Create New Product")
        self.createprod.clicked.connect(self.create_newproduct)
        self.deleteprod= QPushButton ("Delete Product")
        self.editprod = QPushButton ("Edit Product")
        nav_layout.addWidget(self.gomanage)
        nav_layout.addWidget(self.gohome)
        nav_layout.addWidget(self.createprod)
        nav_layout.addWidget(self.deleteprod)
        nav_layout.addWidget(self.editprod)
        
        
        #main_layout.addLayout(nav_layout)
        table_layout.addWidget(self.product_table)
        for btn in [self.gohome, self.gomanage, self.createprod, self.deleteprod, self.editprod]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet(self.button_style)
    def load_products_into_table(self):
        rows = self.db_manager.fetch_product_list()
        product_data = [
            [
                r.get("pid", ""),
                r.get("product_desc", ""),
                f"{float(r['price']):.2f}" if r.get("price") is not None else "",
                r.get("size") or "",
                r.get("category_name") or "",
                r.get("sub_category") or "",
                r.get("size_group") or "",
            ]
            for r in rows
        ]
        # Paint the table
        self.product_table.setRowCount(len(product_data))
        for i, row in enumerate(product_data):
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                #item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.product_table.setItem(i, j, item)
    def gobacktomanagement(self):
        from managementpage import ManagementPage
        self.next_screenacc = ManagementPage(self.username, self.rank)
        self.next_screenacc.show()
        self.hide()
    def create_newproduct(self):
        from createnewproducts import CreateProducts
        self.nextcreate_products = CreateProducts(self.username, self.rank)
        self.nextcreate_products.show()
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
    


