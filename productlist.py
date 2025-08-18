from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QApplication, QTableWidget, QSizePolicy, QHeaderView, QTableView, QTableWidgetItem, QMessageBox
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
        self.selected_pid = None
      
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
        self.deleteprod.clicked.connect(self.on_delete_clicked)
        self.editprod = QPushButton ("Edit Product")
        self.editprod.clicked.connect(self.goto_editproduct)
        nav_layout.addWidget(self.gomanage)
        nav_layout.addWidget(self.gohome)
        nav_layout.addWidget(self.createprod)
        nav_layout.addWidget(self.deleteprod)
        nav_layout.addWidget(self.editprod)
        
        self.product_table.itemSelectionChanged.connect(self.on_row_selected)
        self.product_table.itemSelectionChanged.connect(self.row_selected_foredit)
        #main_layout.addLayout(nav_layout)
        table_layout.addWidget(self.product_table)
        for btn in [self.gohome, self.gomanage, self.createprod, self.deleteprod, self.editprod]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet(self.button_style)
    def on_row_selected(self):
        items = self.product_table.selectedItems()
        if not items:
            self.selected_pid = None
            return
        row = self.product_table.currentRow()
        pid_item = self.product_table.item(row, 0)  # first column = Product ID
        try:
            self.selected_pid = int(pid_item.text())
            print(f"Selected PID: {self.selected_pid}")
        except (ValueError, AttributeError):
            self.selected_pid = None

    def row_selected_foredit(self):
        print("selected for edit here")
        items2 = self.product_table.selectedItems()
        if not items2:
            self.pidfound = None
            return

        row = self.product_table.currentRow()
        try:
            # Grab all columns in that row
            self.pidf        = int(self.product_table.item(row, 0).text())
            self.product_f   = self.product_table.item(row, 1).text()
            self.price_f     = float(self.product_table.item(row, 2).text())
            self.size_f      = self.product_table.item(row, 3).text()
            self.category_f  = self.product_table.item(row, 4).text()
            self.sub_catf    = self.product_table.item(row, 5).text()
            self.size_group  = self.product_table.item(row, 6).text()

            print(f"Selected Product -> "
                f"ID: {self.pidf}, Name: {self.product_f}, Price: {self.price_f}, "
                f"Size: {self.size_f}, Category: {self.category_f}, "
                f"Sub-Category: {self.sub_catf}, Size Group: {self.size_group}")
        except (ValueError, AttributeError) as e:
            print(f"Error reading row: {e}")
            self.pidf = None

    def on_delete_clicked(self):
        if not self.selected_pid:
            QMessageBox.information(self, "Delete Product", "Please select a product to delete.")
            return

        resp = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete product with ID {self.selected_pid}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if resp != QMessageBox.Yes:
            return

        ok = self.db_manager.delete_product(self.selected_pid)
        if ok:
            QMessageBox.information(self, "Deleted", "Product deleted.")
            # refresh table
            self.load_products_into_table()
            self.selected_pid = None
        else:
            QMessageBox.warning(self, "Error", "Failed to delete product.")
    def load_products_into_table(self):
        rows = self.db_manager.fetch_product_list()
        self.product_table.clearContents()
        self.product_table.setRowCount(0)
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

        self.product_table.setRowCount(len(product_data))
        for i, row in enumerate(product_data):
            for j, val in enumerate(row):
                self.product_table.setItem(i, j, QTableWidgetItem(str(val)))
    def goto_editproduct(self):
        from editproducts import EditProducts
        self.editprod = EditProducts(self.username, self.rank, self.pidf, self.product_f, self.price_f, self.size_f, self.category_f, self.sub_catf, self.size_group)
        self.editprod.show()
        self.hide()

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
    


