from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QApplication, QTableWidget, QSizePolicy, QHeaderView, QTableView, QTableWidgetItem, QLineEdit, QComboBox, QCheckBox
from databaseutils import DatabaseManager
from datetime import date
from decimal import Decimal

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
        self.main_category.setStyleSheet("""
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
        """)
        self.create_main_cat = QCheckBox ("Add New Category")
        
        self.sub_category = QComboBox()
        self.sub_category.setStyleSheet("""
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
        """)
        self.create_sub_cat = QCheckBox ("Add New Sub-Category")
        ###
        self.gomanage = QPushButton ("Go Back to Management")
        self.gomanage.clicked.connect(self.gobacktomanagement)
        self.gohome = QPushButton ("Go Back to Orders")
        self.gohome.clicked.connect(self.gobacktohome)
        self.add_sizeoption = QCheckBox("Check to Add Sizes - TBD")
        self.add_vat = QCheckBox("VAT enabled")
        self.checkbox_style = """
                QCheckBox {
                    font-size: 13px;
                    font-family: 'Segoe UI', sans-serif;
                    color: black;
                                             
                    background-color: transparent;
                    border: none;
                    padding: 6px;
                    text-align: center;
                }

                QCheckBox::indicator {
                    width: 1.15em;
                    height: 1.15em;
                   
                    border: 0.06em solid rgba(0, 0, 0, 0.275);
                    border-radius: 0.2em;
                    background-color: white;
                    
                    
                }

                QCheckBox::indicator:checked {
                    background-color: #3B99FC;
                    border-color: #3B99FC;
                }

                QCheckBox::indicator:checked::after {
                    color: white;
                    font-size: 1em;
                    position: relative;
                    left: 0.25em;
                    top: 0.1em;
                }

                QCheckBox::indicator:pressed {
                    background-color: #f0f0f0;
                    
                }

                QCheckBox::indicator:checked:pressed {
                    background-color: #0a7ffb;
                }

                QCheckBox::indicator:focus {
                    
                }

                QCheckBox::indicator:disabled {
                    opacity: 0.5;
                }

                QCheckBox::indicator:unchecked {
                    background-color: white;
                }

                QCheckBox::indicator:unchecked:hover {
                    background-color: #f0f0f0;
                }

                QCheckBox::indicator:unchecked:pressed {
                    background-color: #f0f0f0;
                }
                """
        self.price_box = QLineEdit()
        self.price_box.setPlaceholderText("Enter Product Price")
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
        self.finalize_product.clicked.connect(self.insert_product)
        

        self.holder_label = QLabel(f"TBD")
        self.holder_label.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px")

        exit_layout.addWidget(self.gomanage)
        exit_layout.addWidget(self.gohome)
        header_layout.addWidget(self.product_box)
        header_layout.addWidget(self.holder_label)
        category_layout.addWidget(self.main_category)
        category_layout.addWidget(self.create_main_cat)
        category_layout.addWidget(self.sub_category)
        category_layout.addWidget(self.create_sub_cat)
        
        bottom_layout.addWidget(self.add_sizeoption)
        bottom_layout.addWidget(self.add_vat)
        
        bottom_layout.addWidget(self.price_box)
        bottom_layout.addWidget(self.finalize_product)
        main_layout.addLayout(exit_layout)
        main_layout.addLayout(header_layout)
        main_layout.addLayout(category_layout)
        main_layout.addLayout(bottom_layout)
        self.create_main_cat.stateChanged.connect(self.toggle_editable_catbox)
        self.create_sub_cat.stateChanged.connect(self.toggle_editable_subcatbox)
        for chkbox in [self.add_sizeoption, self.create_main_cat, self.create_sub_cat, self.add_vat]:
            chkbox.setMinimumHeight(40)
            chkbox.setStyleSheet(self.checkbox_style)
        
        for btn in [self.gohome, self.gomanage, self.finalize_product]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet(self.button_style)
        self.enter_new_category()
    
    
    def toggle_editable_catbox(self, state):

        if self.create_main_cat.isChecked():
            print('editable')
            self.main_category.setEditable(True)  # Start in searchable mode
            self.main_category.setInsertPolicy(QComboBox.NoInsert)
            self.main_category.setEditText("")
            self.main_category.setStyleSheet("""
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
""")
           
        else:
            print('not editable')
            self.main_category.setEditable(False)
    def toggle_editable_subcatbox(self, state):

        if self.create_sub_cat.isChecked():
            print('editable')
            self.sub_category.setEditable(True)  # Start in searchable mode
            self.sub_category.setInsertPolicy(QComboBox.NoInsert)
            self.sub_category.setEditText("")
            self.sub_category.setStyleSheet("""
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
""")
           
        else:
            print('not editable')
            self.sub_category.setEditable(False)        
    def insert_product(self):
        if self.add_sizeoption.isChecked():
            print("Go to other page - TBD for now")
        if self.add_vat.isChecked():
            self.vatv = "yes"
        else: 
            self.vatv = "no"
        pname = self.product_box.text().strip()
        catused  = self.main_category.currentText().strip()
        subused  = self.sub_category.currentText().strip()
        price_txt = self.price_box.text().strip()
        

        # very light validation
        if not pname or not price_txt:
            print("Missing product name or price.")
            return

        try:
            price = Decimal(price_txt)
        except ValueError:
            print("Price must be a number.")
            return

        new_id = self.db_manager.insert_product(
            product_desc=pname,
            price=price,
            category_name=catused,
            sub_category=subused,
            vat = self.vatv, 
            size="No Size",
            size_group="No Size",
            
        )

        if new_id:
            print(f"Inserted product id={new_id}")
            # optional: clear inputs
            # self.product_box.clear(); self.price_box.clear()
        else:
            print("Insert failed.")
        from productlist import ProductPage
        self.next_screenproducts = ProductPage(self.username, self.rank)
        self.next_screenproducts.show()
        self.hide()
    def enter_new_category(self):
        cats = self.db_manager.fetch_categories_for_orders()
        cats = [c for c in cats if c != "All"]
        cats = ["Select A Category"] + cats  
        self.main_category.clear()
        self.main_category.addItems(cats)
        self.main_category.currentIndexChanged.connect(self.load_subcategories)

    def load_subcategories(self):
        
        
        cat = self.main_category.currentText().strip()
        self.sub_category.clear()
        if not cat:
            return

        subs = self.db_manager.fetch_subcategories_by_category(cat)
        
        subs = [s for s in subs if s != "All"]

        self.sub_category.addItems(subs)
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
    


