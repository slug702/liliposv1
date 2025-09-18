from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QLineEdit,
    QSizePolicy, QComboBox, QTableWidget, QTableWidgetItem, QTableView, QSpacerItem, QGridLayout, QFrame, QHeaderView
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from databaseutils import DatabaseManager
from managementpage import ManagementPage
from decimal import Decimal

class POSHomePage(QWidget):
    def __init__(self, username, rank, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Orders - Lili Systems")
        self.username = username
        self.rank = rank
        self.showMaximized()
        self.setStyleSheet("background-color: #f2f2f2;")
        self.db_manager = DatabaseManager()
        # === BUTTON STYLE ===
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

        self.category_button_style = """
        QPushButton {
            background-color: white;
            color: #000000;
            border: 2px solid #1877F2;
            border-radius: 12px;
            padding: 14px 24px;
            font-size: 16px;
            font-family: 'Segoe UI', sans-serif;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #f0f8ff;
        }
        QPushButton:pressed {
            background-color: #e6f2ff;
        }
        """
        self.combobox_style = """
        QComboBox {
            background-color: #FFFFFF;
            color: #202124;
            font-size: 16px;
            font-family: 'Segoe UI', sans-serif;
            border: 2px solid #EBEBEB;  /* Thinner border */
            border-radius: 14px;
            padding: 9px 17px;  /* Keep dimensions consistent */
        }
        QComboBox:focus {
            border: 1px solid #1877F2;
            background-color: #f5faff;
            outline: none;
        }
        QComboBox::drop-down {
            width: 0px;
        }
        QComboBox QAbstractItemView {
            background-color: #FFFFFF;
            color: #202124;
            selection-background-color: #E8EAE6;
            border: 1px solid #EBEBEB;
            border-radius: 8px;
        }
        """

        

        # === TOP CATEGORY BAR with ARROWS ===
        self.category_scroll = QScrollArea()
        self.category_scroll.setWidgetResizable(True)
        self.category_scroll.setFrameShape(QFrame.NoFrame)
        self.category_bar_widget = QWidget()
        self.category_bar_layout = QHBoxLayout(self.category_bar_widget)
        
        self.category_bar_layout.setSpacing(10)
        self.category_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.category_scroll.setWidget(self.category_bar_widget)
        #self.category_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.category_scroll.setFixedHeight(60)

       

        # Load categories into bar
        self.load_categories()

        top_category_layout = QHBoxLayout()
        
        top_category_layout.addWidget(self.category_scroll)
     

        # === SUB-CATEGORY + SEARCH ===
        self.sub_category = QComboBox()
        self.sub_category.setStyleSheet(self.combobox_style)
        self.sub_category.addItem("Select Category")
        self.sub_category.setEnabled(False)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        self.search_box.setStyleSheet("""
        QLineEdit {
            background-color: #FFFFFF;
            color: #202124;
            border: 2px solid #EBEBEB;  /* Thinner border */
            border-radius: 14px;
            font-size: 16px;
            font-family: 'Segoe UI', sans-serif;
            padding: 9px 17px;
        }
        QLineEdit:focus {
            border: 1px solid #1877F2;
            background-color: #f5faff;
        }
        """)

        self.search_btn = QPushButton("Search")
        self.search_btn.setStyleSheet(self.button_style)
        filters_layout = QHBoxLayout()
        filters_layout.addWidget(self.sub_category)
        filters_layout.addWidget(self.search_box)
        filters_layout.addWidget(self.search_btn)
        self.search_btn.clicked.connect(self.load_products_with_search)
        # === ORDER SUMMARY CART ===
        self.order_table = QTableWidget(0, 4)
        self.order_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.order_table.setHorizontalHeaderLabels(["id", "product", "price", "discount"])
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



        #goback here
        self.label_stylesheet = ("""
            font-size: 20px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            color: #111827;
        """)
        self.vatable_label = QLabel("VATable Sales:")
        self.vatable_label.setStyleSheet(self.label_stylesheet)
        self.discounts_label = QLabel("Total Discount: ")
        self.discounts_label.setStyleSheet(self.label_stylesheet)
        self.vat_label = QLabel("VAT Total: ")
        self.vat_label.setStyleSheet(self.label_stylesheet)
        self.total_label = QLabel("Amount Payable:")
        self.total_label.setStyleSheet(self.label_stylesheet)
        
        self.btn_discount = QPushButton("add discount")
        self.btn_place = QPushButton("pay order")
        for btn in [self.btn_discount, self.btn_place]:
            btn.setStyleSheet(self.button_style)
        self.ordernumber = QComboBox()
        self.reload_unpaid_invoices()
        
        self.ordernumber.setStyleSheet(self.combobox_style)
        ordnum = self.ordernumber.currentText()
        self.ordernumber.currentIndexChanged.connect(self.update_header)
        self.header2 = QLabel(f"Order Number: {ordnum}")
        self.header3 = QLabel(f"Table Number: {"TBD"}")
        self.header2.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px")
        self.header3.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px")
        order_layout = QVBoxLayout()

        # Let the table grow to fill vertical space
        order_layout.addWidget(self.header2)
        order_layout.addWidget(self.header3)
        order_layout.addWidget(self.order_table)  # no alignment flag
        order_layout.addStretch()  # pushes the rest to the bottom

        order_layout.addWidget(self.vatable_label)
        order_layout.addWidget(self.discounts_label)
        order_layout.addWidget(self.vat_label)
        order_layout.addWidget(self.total_label)
        order_layout.addWidget(self.btn_discount)
        order_layout.addWidget(self.btn_place)

        # === LEFT NAVIGATION (TOP & BOTTOM) ===
        
        
        self.gotoinventory = QPushButton ("Inventory - TBD")
        self.gotosettings = QPushButton ("Settings")
        self.gotomanagement = QPushButton ("Management")
        self.viewtables = QPushButton("View/Select Tables - TBD")
        self.createorder = QPushButton("Create Order")
        self.createorder.clicked.connect(self.insert_new_invoice) #goback
        
        #self.addorderbtn = QPushButton("Add Product")
        self.removebtn = QPushButton("Remove")
        self.removebtn.setStyleSheet(self.button_style)
        self.removebtn.clicked.connect(self.remove_selected_transaction)
        self.combobtn = QPushButton("Create Combo Meal - TBD")
        btn.setStyleSheet(self.button_style)
        nav_layout = QVBoxLayout()
       
        nav_layout.addWidget(self.gotoinventory)
        
       
        nav_layout.addWidget(self.gotomanagement)
        nav_layout.addWidget(self.gotosettings)
        self.gotomanagement.clicked.connect(self.show_management)
            
        nav_layout.addStretch()
        nav_layout.addWidget(self.viewtables, alignment=Qt.AlignLeft)
        nav_layout.addWidget(self.createorder, alignment=Qt.AlignLeft)
        nav_layout.addWidget(self.ordernumber, alignment=Qt.AlignLeft)
        #nav_layout.addWidget(self.addorderbtn, alignment=Qt.AlignLeft)
        nav_layout.addWidget(self.removebtn, alignment=Qt.AlignLeft)
        nav_layout.addWidget(self.combobtn, alignment=Qt.AlignLeft)
        for btn in [self.gotoinventory, self.gotosettings, self.gotomanagement, self.combobtn, self.createorder, self.viewtables]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet(self.button_style)    
        
        # === CENTRAL COMPOSITION ===
        self.center_content = QVBoxLayout()
        self.center_content.addLayout(filters_layout)
        

        main_content = QHBoxLayout()
        main_content.addLayout(nav_layout, 1)
        main_content.addLayout(self.center_content, 4)
        main_content.addLayout(order_layout, 2)
        # === HEADER ===
       
        
        main_layout = QVBoxLayout()
       
       
        main_layout.addLayout(top_category_layout)
        main_layout.addLayout(main_content)
        self.load_products()
        
        self.sub_category.currentIndexChanged.connect(self.handle_subcategory_change)
        self.setLayout(main_layout)

    # === Placeholder: Load categories dynamically ===
    def reciept_calculations():
        return

    def remove_selected_transaction(self):
        row = self.order_table.currentRow()
        if row < 0:
            print("Select a line to remove.")
            return
        item = self.order_table.item(row, 0)  # tr_id column
        if not item:
            return
        tr_id_txt = item.text().strip()
        if not tr_id_txt.isdigit():
            print("Invalid tr_id.")
            return

        ok = self.db_manager.delete_transaction(int(tr_id_txt))
        if ok:
            self.reload_order_table()
        else:
            print("Delete failed.")

    def reload_order_table(self):
        inv_id = self.ordernumber.currentText().strip()
        self.order_table.setRowCount(0)
        if not inv_id.isdigit():
            return

        rows = self.db_manager.fetch_transactions_for_invoice(int(inv_id))
        for r in rows:
            i = self.order_table.rowCount()
            self.order_table.insertRow(i)
            self.order_table.setItem(i, 0, QTableWidgetItem(str(r.get("tr_id") or "")))
            self.order_table.setItem(i, 1, QTableWidgetItem(str(r.get("tr_desc") or "")))
            self.order_table.setItem(i, 2, QTableWidgetItem("" if r.get("gross_price") is None else str(r["gross_price"])))
            self.order_table.setItem(i, 3, QTableWidgetItem("" if r.get("discount_rate") is None else str(r["discount_rate"])))


    def insert_new_invoice(self):
        new_id = self.db_manager.insert_invoice_new()
        if new_id:
            # refresh the combo and select the new invoice
            self.reload_unpaid_invoices()
            self.ordernumber.setCurrentText(str(new_id))
            self.update_header()
        else:
            print("Failed to create invoice.")
        #insert new invoice here, put "new" in the status column. nothing else for the rest
        return
    def reload_unpaid_invoices(self):
  
        self.ordernumber.clear()

        try:
            inv_ids = self.db_manager.fetch_unpaid_invoice_ids()  # from DatabaseManager
            if inv_ids:
                self.ordernumber.addItems(inv_ids)
        except Exception as e:
            print(f"Could not load unpaid invoices: {e}")

    
    
    def update_header(self):
        self.reload_order_table()
        selected_order = self.ordernumber.currentText()
        self.header2.setText(f"Order Number: {selected_order}")
    def load_categories(self):
        # Clear existing buttons
        
        
        categories = self.db_manager.fetch_categories_for_orders()
        for name in categories:
            btn = QPushButton(name)
            btn.setStyleSheet(self.category_button_style)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, n=name: self.handle_category_click(n))  # Connect button to handler
            self.category_bar_layout.addWidget(btn)

    # === Placeholder: Load subcategories dynamically ===
    def handle_subcategory_change(self):
        
        subcat = self.sub_category.currentText()
        self.subcattopass = self.sub_category.currentText()
        self.load_products_with_filters_and_sub()
        print(f"Selected sub-category changed to: {subcat}")
    
    def load_products_with_filters_and_sub(self):
        self.clear_center_content()
        self.product_grid = QGridLayout()

        all_products = self.db_manager.fetch_products_by_category_and_sub(
            self.category_picked,
            self.subcattopass
        )

        for idx, (name, price) in enumerate(all_products):
            btn = QPushButton(f"{name}     ₱{price}")
            btn.setFixedSize(150, 60)  # consistent size
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    padding: 8px;
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 6px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)

            self.product_grid.addWidget(btn, idx // 4, idx % 4)

            # Print both name and price on click
            btn.clicked.connect(lambda checked, n=name, p=price: print(f"Product clicked: {n} - ₱{p}"))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        scroll.viewport().setStyleSheet("background-color: transparent; border: none;")
        scroll.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setLayout(self.product_grid)
        container.setStyleSheet("background-color: transparent; border: none;")
        container.setContentsMargins(0, 0, 0, 0)

        self.product_grid.setContentsMargins(0, 0, 0, 0)
        self.product_grid.setSpacing(12)

        scroll.setWidget(container)
        self.center_content.addWidget(scroll)
        
    def load_products(self):
        self.clear_center_content()
        self.product_grid = QGridLayout()
        all_products = self.db_manager.fetch_all_products()
        for idx, row in enumerate(all_products):
            name = row['product_desc']
            price = row['price']

            btn = QPushButton(f"{name}     ₱{price}")
            btn.setFixedSize(150, 60)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    padding: 8px;
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 6px;
                    text-align: left;
                }
                QPushButton:hover { background-color: #e0e0e0; }
            """)

            self.product_grid.addWidget(btn, idx // 4, idx % 4)

            # capture the row for this button and insert on click
            btn.clicked.connect(lambda _=False, prod=row: self.add_item_to_current_invoice(prod))


        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        scroll.viewport().setStyleSheet("background-color: transparent; border: none;")
        scroll.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setLayout(self.product_grid)
        container.setStyleSheet("background-color: transparent; border: none;")
        container.setContentsMargins(0, 0, 0, 0)

        self.product_grid.setContentsMargins(0, 0, 0, 0)
        self.product_grid.setSpacing(12)

        scroll.setWidget(container)
        self.center_content.addWidget(scroll)
    def add_item_to_current_invoice(self, prod):
        inv_id = self.ordernumber.currentText().strip()
        if not inv_id or not inv_id.isdigit():
            print("Select an order number first.")
            return

        ok = self.db_manager.insert_transaction_item(
            inv_id=int(inv_id),
            pid=prod['pid'],
            desc=prod['product_desc'],
            price=prod['price'],
            vat=prod['vat'],       # your products.vat (e.g., 'yes'/'no' or 0/1)
        )
        if ok:
            print(f"Added {prod['product_desc']} (₱{prod['price']}) to invoice {inv_id}")
            self.reload_order_table()
        else:
            print("Failed to add item.")

        
    def load_products_with_search(self):
        
        
        self.sub_category.setEnabled(False)
        self.sub_category.clear()
        self.sub_category.addItem("Select Category")
        search_term = self.search_box.text().strip()
        self.clear_center_content()
        self.product_grid = QGridLayout()
        all_products = self.db_manager.fetch_products_with_search(search_term)

        for idx, (name, price) in enumerate(all_products):
            btn = QPushButton(f"{name}     ₱{price}")
            btn.setFixedSize(150, 60)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    padding: 8px;
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 6px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            self.product_grid.addWidget(btn, idx // 4, idx % 4)
            btn.clicked.connect(lambda checked, n=name, p=price: print(f"Product clicked: {n} - ₱{p}"))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        scroll.viewport().setStyleSheet("background-color: transparent; border: none;")
        scroll.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setLayout(self.product_grid)
        container.setStyleSheet("background-color: transparent; border: none;")
        container.setContentsMargins(0, 0, 0, 0)

        self.product_grid.setContentsMargins(0, 0, 0, 0)
        self.product_grid.setSpacing(12)

        scroll.setWidget(container)
        self.center_content.addWidget(scroll)
        
    def load_products_with_filters(self):
        self.clear_center_content()
        self.product_grid = QGridLayout()
        self.load_subcategories(self.category_picked)
        all_products = self.db_manager.fetch_all_products_with_filter(self.category_picked)

        for idx, (name, price) in enumerate(all_products):
            btn = QPushButton(f"{name}     ₱{price}")
            btn.setFixedSize(150, 60)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    padding: 8px;
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 6px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            self.product_grid.addWidget(btn, idx // 4, idx % 4)
            btn.clicked.connect(lambda checked, n=name, p=price: print(f"Product clicked: {n} - ₱{p}"))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        scroll.viewport().setStyleSheet("background-color: transparent; border: none;")
        scroll.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setLayout(self.product_grid)
        container.setStyleSheet("background-color: transparent; border: none;")
        container.setContentsMargins(0, 0, 0, 0)

        self.product_grid.setContentsMargins(0, 0, 0, 0)
        self.product_grid.setSpacing(12)

        scroll.setWidget(container)
        self.center_content.addWidget(scroll)

    def handle_category_click(self, category_name):
        self.sub_category.setEnabled(True)
        print(f"Filtering products by category: {category_name}")
        self.category_picked = category_name

        if category_name == "All":
            self.sub_category.setEnabled(False)
            self.sub_category.clear()
            self.sub_category.addItem("Select Category")
            self.load_products()
        else:
            self.load_subcategories(category_name)
            self.subcattopass = self.sub_category.currentText()
            self.load_products_with_filters_and_sub()
    def clear_center_content(self):
        for i in reversed(range(self.center_content.count())):
            widget_item = self.center_content.itemAt(i)
            widget = widget_item.widget()
            if widget is not None:
                widget.setParent(None)
    def load_subcategories(self, category_name):
        self.sub_category.clear()
        
        subcategories = self.db_manager.fetch_subcategories_by_category(category_name)
        print(subcategories)
        # Always include "All" as first option
        self.sub_category.addItem("All")
        print("loaded subcategories here")
        self.sub_category.addItems(subcategories)
        self.sub_category.setCurrentIndex(0)
        self.subcattopass = "All"
    def show_management(self):
        self.management_next = ManagementPage(self.username, self.rank)
        self.management_next.show()
        self.hide()



