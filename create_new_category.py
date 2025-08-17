from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QApplication, QTableWidget, QSizePolicy, QHeaderView, QTableView, QTableWidgetItem, QLineEdit, QComboBox, QCheckBox
from databaseutils import DatabaseManager
from datetime import date

class CreateProducts(QWidget):
    def __init__(self, username, rank, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Product - Lili Systems")
        self.username = username
        self.rank = rank
        #self.showMaximized()
        self.resize(700, 300)
        #self.center_window()
        # Header
       
        self.date_today = date.today()
        
        
        self.db_manager = DatabaseManager()

      
        # Main area (will swap out widgets here)
        #self.main_area = QLabel("Select a section above to begin.")
        #self.main_area.setStyleSheet("font-size: 20px; color: gray; margin-top: 40px; font-family: 'Segoe UI', sans-serif")

        main_layout = QVBoxLayout(self)
        exit_layout = QHBoxLayout(self)
        header_layout = QHBoxLayout(self)
        bottom_layout = QHBoxLayout(self)
        # === ORDER SUMMARY CART ===
        category_layout = QHBoxLayout(self)
        

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



        
        
        self.product_box = QLineEdit()
        self.product_box.setPlaceholderText("Enter Product Name")
        self.product_box.setStyleSheet("""
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
        self.main_category = QComboBox()
        self.create_main_cat = QPushButton ("Add New Category")
        
        self.sub_category = QComboBox()
        self.create_sub_cat = QPushButton ("Add New Sub-Category")
        ###
        self.gomanage = QPushButton ("Go Back to Management")
        self.gomanage.clicked.connect(self.gobacktomanagement)
        self.gohome = QPushButton ("Go Back to Orders")
        self.gohome.clicked.connect(self.gobacktohome)
        self.add_sizeoption = QCheckBox("Check to Add Sizes")
        self.price_box = QLineEdit()
        self.price_box.setPlaceholderText("Enter Product Product")
        self.price_box.setStyleSheet("""
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
        self.finalize_product = QPushButton ("Finalize Product Creation")
        

        self.holder_label = QLabel(f"TBD")
        self.holder_label.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px")

        exit_layout.addWidget(self.gomanage)
        exit_layout.addWidget(self.gohome)
        header_layout.addWidget(self.product_box)
        header_layout.addWidget(self.holder_label)
        category_layout.addWidget(self.main_category)
        category_layout.addWidget(self.create_main_cat)
        category_layout.addWidget(self.create_sub_cat)
        category_layout.addWidget(self.sub_category)
        bottom_layout.addWidget(self.add_sizeoption)
        bottom_layout.addWidget(self.price_box)
        bottom_layout.addWidget(self.finalize_product)
        main_layout.addLayout(exit_layout)
        main_layout.addLayout(header_layout)
        main_layout.addLayout(category_layout)
        main_layout.addLayout(bottom_layout)

        
        
        for btn in [self.gohome, self.gomanage, self.create_main_cat, self.create_sub_cat]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet(self.button_style)
   
    def gobacktomanagement(self):
        from managementpage import ManagementPage
        self.next_screenacc = ManagementPage(self.username, self.rank)
        self.next_screenacc.show()
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
    


