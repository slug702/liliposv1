from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QLineEdit,
    QSizePolicy, QComboBox, QTableWidget, QTableWidgetItem, QTableView, QSpacerItem, QGridLayout, QFrame, QHeaderView
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from databaseutils import DatabaseManager

class POSHomePage(QWidget):
    def __init__(self, username, rank, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Orders - Lili's Systems")
        self.username = username
        self.rank = rank
        self.showMaximized()
        self.setStyleSheet("background-color: #f2f2f2;")
        self.db_manager = DatabaseManager()
        # === BUTTON STYLE ===
        self.button_style = """
            QPushButton {
                background-color: #E8EAE6;
                border: 2px solid #D3D3D3;
                border-radius: 10px;
                color: #111827;
                font-family: 'Segoe UI', sans-serif;
                font-size: 15px;
                font-weight: 600;
                padding: 10px 16px;
            }
            QPushButton:hover {
                background-color: #D1D3D4;
            }
            QPushButton:pressed {
                background-color: #BCC0C4;
            }
        """
        self.combobox_style = """
    QComboBox {
        font-size: 18px;  /* Font size for consistency */
        font-family: 'Segoe UI', sans-serif;  /* Matching font family */
        color: #202124;  /* Darker text color */
        background-color: #FFFFFF;  /* Pure white background */
        border-radius: 12px;  /* Larger border radius for a more rounded appearance */
        padding: 7px 15px;  /* Padding for better spacing */
        border: 2px solid #D3D3D3;  /* Light gray border */
        
    }

    QComboBox:focus {
        border: 2px solid #1877F2;  /* Sage green border on focus */
        outline: none;  /* Remove default outline */
    }

    QComboBox::drop-down {
        width: 0px;  /* Hide the drop-down arrow */
    }

    QComboBox QAbstractItemView {
        color: #202124;  /* Darker text color for list items */
        background-color: #FFFFFF;  /* White background for the drop-down list */
        selection-background-color: #E8EAE6;  /* Light neutral background color when an item is selected */
        border: 1px solid #D3D3D3;  /* Border for the drop-down list */
        border-radius: 8px;  /* Slightly rounded corners for the drop-down list */
    }
"""

        

        # === TOP CATEGORY BAR with ARROWS ===
        self.category_scroll = QScrollArea()
        self.category_scroll.setWidgetResizable(True)
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
        self.sub_category.addItems(['Sub-Categories'])
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                border: 2px solid #D3D3D3;
                border-radius: 10px;
                font-size: 16px;
                padding: 6px 12px;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border: 2px solid #1877F2;
            }
        """)
        self.search_btn = QPushButton("Search")
        self.search_btn.setStyleSheet(self.button_style)
        filters_layout = QHBoxLayout()
        filters_layout.addWidget(self.sub_category)
        filters_layout.addWidget(self.search_box)
        filters_layout.addWidget(self.search_btn)
        
        # === PRODUCT GRID ===
        self.product_grid = QGridLayout()
        all_products = self.db_manager.fetch_all_products()
        # === PRODUCT GRID ===
        self.product_grid = QGridLayout()
        all_products = self.db_manager.fetch_all_products()

        for idx, name in enumerate(all_products):
            btn = QPushButton(name)
            btn.setFixedSize(150, 60)  # consistent size
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    padding: 8px;
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            
            # connect to future slot if needed
            # btn.clicked.connect(lambda checked, n=name: self.handle_product_click(n))

            self.product_grid.addWidget(btn, idx // 4, idx % 4)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(self.product_grid)
        scroll.setWidget(container)

        # === ORDER SUMMARY CART ===
        self.order_table = QTableWidget(5, 3)
        self.order_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.order_table.setHorizontalHeaderLabels(["quantity", "name", "price"])
        self.order_table.verticalHeader().setVisible(False)
        self.order_table.setSelectionBehavior(QTableView.SelectRows)
        self.order_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.order_table.setStyleSheet("""
          QTableWidget {
                border: 0px solid #000000; /*  borders for structure */
                background-color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif; /* Consistent font across the interface */
            }

            
            QHeaderView::section {
                background-color: #F5F5F5; /* Lighter gray for headers */
                padding: 2px 8px; /* Reduced padding for a sleeker look */
                border: none; /* Remove border for a flatter design */
                border-radius: 4px;
                font-size: 14px; /* Smaller font size */
                color: #333; /* Darker text color for better contrast */
            }

            

                        QTableCornerButton::section {
                    background: #F5F5F5; /* Light gray background for the corner button */
                    border: 1px solid #D3D3D3; /* Light gray border */
                    border-radius: 4px; /* Slightly rounded corners */
                }

                QScrollBar:vertical {
                    border: none;
                    background: #E8EAE6; /* Light neutral background color for the scrollbar */
                    width: 14px;
                    margin: 18px 0 18px 0;
                }

                QScrollBar::handle:vertical {
                    background: #BCC0C4; /* Slightly darker gray for the scrollbar handle */
                    min-height: 20px;
                    border-radius: 7px; /* Rounded handle for a modern look */
                }

                QScrollBar::add-line:vertical {
                    background: #D1D3D4; /* Slightly darker for the add line control */
                    height: 14px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                    border-radius: 7px;
                }

                QScrollBar::sub-line:vertical {
                    background: #D1D3D4; /* Slightly darker for the sub line control */
                    height: 14px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                    border-radius: 7px;
                }
        """)

        order_data = [["3", "meal3", "3"], ["3", "fried chicken", "3"], ["3", "burger", "3"]]
        for i, row in enumerate(order_data):
            for j, val in enumerate(row):
                self.order_table.setItem(i, j, QTableWidgetItem(val))

        self.total_label = QLabel("total:")
        self.total_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 10px")

        self.btn_discount = QPushButton("add discount")
        self.btn_place = QPushButton("place order")
        for btn in [self.btn_discount, self.btn_place]:
            btn.setStyleSheet(self.button_style)

        order_layout = QVBoxLayout()

        # Let the table grow to fill vertical space
        order_layout.addWidget(self.order_table)  # no alignment flag
        order_layout.addStretch()  # pushes the rest to the bottom

        order_layout.addWidget(self.total_label)
        order_layout.addWidget(self.btn_discount)
        order_layout.addWidget(self.btn_place)

        # === LEFT NAVIGATION (TOP & BOTTOM) ===
        
        self.gotoorders = QPushButton ("Orders")
        self.gotoinventory = QPushButton ("Inventory")
        self.gotosettings = QPushButton ("Setting")
        self.gotoreports = QPushButton ("Report")
        self.gotoadmin = QPushButton ("Admin")

        self.viewtables = QPushButton("View/Select Tables")
        self.createorder = QPushButton("Create Order")
        self.ordernumber = QComboBox()
        dummy_ordernum = ("Select Order", "1", "2")
        self.ordernumber.addItems(dummy_ordernum)
        self.ordernumber.setStyleSheet(self.combobox_style)
        ordnum = self.ordernumber.currentText()
        self.ordernumber.currentIndexChanged.connect(self.update_header)
        self.addorderbtn = QPushButton("Add Product")
        self.removebtn = QPushButton("Remove")
        self.removebtn.setStyleSheet(self.button_style)
        self.combobtn = QPushButton("Create Combo Meal")
        btn.setStyleSheet(self.button_style)
        nav_layout = QVBoxLayout()
        nav_layout.addWidget(self.gotoorders)
        nav_layout.addWidget(self.gotoinventory)
        nav_layout.addWidget(self.gotosettings)
        nav_layout.addWidget(self.gotoreports)
        nav_layout.addWidget(self.gotoadmin)
            
        nav_layout.addStretch()
        nav_layout.addWidget(self.viewtables, alignment=Qt.AlignLeft)
        nav_layout.addWidget(self.createorder, alignment=Qt.AlignLeft)
        nav_layout.addWidget(self.ordernumber, alignment=Qt.AlignLeft)
        nav_layout.addWidget(self.addorderbtn, alignment=Qt.AlignLeft)
        nav_layout.addWidget(self.removebtn, alignment=Qt.AlignLeft)
        nav_layout.addWidget(self.combobtn, alignment=Qt.AlignLeft)
        for btn in [self.gotoorders, self.gotoinventory, self.gotosettings, self.gotoreports, self.gotoadmin, self.addorderbtn, self.combobtn, self.createorder, self.viewtables]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet(self.button_style)    
        
        # === CENTRAL COMPOSITION ===
        center_content = QVBoxLayout()
        center_content.addLayout(filters_layout)
        center_content.addWidget(scroll)

        main_content = QHBoxLayout()
        main_content.addLayout(nav_layout, 1)
        main_content.addLayout(center_content, 4)
        main_content.addLayout(order_layout, 2)
        # === HEADER ===
        header_layout = QHBoxLayout()
        self.header = QLabel(f"Welcome, {username}! ")
        self.header2 = QLabel(f"Order Number: {ordnum}")
        self.header3 = QLabel(f"Table Number: {"TBD"}")
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px")
        self.header2.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px")
        self.header3.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px")
        main_layout = QVBoxLayout()
        header_layout.addWidget(self.header)
        header_layout.addWidget(self.header2, alignment=Qt.AlignLeft)
        header_layout.addWidget(self.header3, alignment=Qt.AlignLeft)
        main_layout.addLayout(header_layout)
        main_layout.addLayout(top_category_layout)
        main_layout.addLayout(main_content)
        
        self.setLayout(main_layout)

    # === Placeholder: Load categories dynamically ===
    def update_header(self):
        selected_order = self.ordernumber.currentText()
        self.header2.setText(f"Order Number: {selected_order}")
    def load_categories(self):
        # Clear existing buttons
        

        categories = self.db_manager.fetch_categories_for_orders()
        for name in categories:
            btn = QPushButton(name)
            btn.setStyleSheet(self.button_style)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, n=name: self.handle_category_click(n))  # Connect button to handler
            self.category_bar_layout.addWidget(btn)

    # === Placeholder: Load subcategories dynamically ===
    def handle_category_click(self, category_name):
        print(f"Filtering products by category: {category_name}")
        #self.display_products(category_name) #THIS WILL BE THE ONE TO CHANGE THE CURRENT CATEGORIES SHOWN
    def load_subcategories(self, category_name):
        self.sub_category.clear()
        if category_name == "Mains":
            self.sub_category.addItems(["Rice Meal", "Pasta", "Grilled"])
        else:
            self.sub_category.addItems(["Option 1", "Option 2", "Option 3"])


