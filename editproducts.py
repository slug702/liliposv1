from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QApplication, QTableWidget, QSizePolicy, QHeaderView, QTableView, QTableWidgetItem, QLineEdit, QComboBox, QCheckBox
from databaseutils import DatabaseManager
from PySide6.QtCore import Qt
from datetime import date
from decimal import Decimal
class EditProducts(QWidget):
    
    def __init__(self, username, rank, pidf, product_f, price_f, size_f, category_f, sub_catf, size_group, parent=None ):
        super().__init__(parent)
        self.setWindowTitle("Edit Selected Product - Lili Systems")
        self.username = username
        self.rank = rank
        self.resize(700, 300)
        self.date_today = date.today()
        self.db_manager = DatabaseManager()
        self.resize(700, 300)
        self.date_today = date.today()
        self.db_manager = DatabaseManager()

        # store the incoming values (so you can also use them later when saving)
        self.pidf       = pidf
        self.product_f  = product_f
        self.price_f    = price_f
        self.size_f     = size_f
        self.category_f = category_f
        self.sub_catf   = sub_catf
        self.size_group = size_group
    
       

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
        self.product_box = QLineEdit()
        self.product_box.setText(self.product_f or "")
        try:
            self.price_box.setText(f"{Decimal(self.price_f):.2f}")
        except Exception:
            self.price_box.setText(str(self.price_f) if self.price_f is not None else "")
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
        self.gohome = QPushButton ("Go Back to Product List")
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
       
        self.finalize_product = QPushButton ("Save Changes to Product")
        self.finalize_product.clicked.connect(self.edit_products)
        

        self.holder_label = QLabel(f"TBD")
        self.holder_label.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px")

        
        exit_layout.addWidget(self.gohome)
        exit_layout.addWidget(self.gomanage)
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
        self.enter_new_category()           # populates main_category
        self._select_current_category()     # NEW: pick the incoming category in the combo
        self._select_current_subcategory()
    def _select_current_category(self):
        # Select current category if it exists in the model
        if self.category_f:
            i = self.main_category.findText(self.category_f, Qt.MatchFixedString)
            if i >= 0:
                # setting the index will trigger load_subcategories via your signal
                self.main_category.setCurrentIndex(i)
            else:
                # if not found and you want it typed-in when editable is on:
                if self.create_main_cat.isChecked():
                    self.main_category.setEditable(True)
                    self.main_category.setEditText(self.category_f)

    def _select_current_subcategory(self):
        # ensure subcategories are loaded for the selected main category
        self.load_subcategories()
        if self.sub_catf:
            j = self.sub_category.findText(self.sub_catf, Qt.MatchFixedString)
            if j >= 0:
                self.sub_category.setCurrentIndex(j)
            else:
                if self.create_sub_cat.isChecked():
                    self.sub_category.setEditable(True)
                    self.sub_category.setEditText(self.sub_catf)
    
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
    def edit_products(self):
        # If you’re using size options elsewhere, keep the early exit
        if self.add_sizeoption.isChecked():
            print("Go to other page - TBD for now")
        if self.add_vat.isChecked():
            self.vatv = "yes"
        else: 
            self.vatv = "no"
        # Grab current UI values
        pname    = self.product_box.text().strip()
        catused  = self.main_category.currentText().strip()
        subused  = self.sub_category.currentText().strip()
        price_txt= self.price_box.text().strip()

        # very light validation
        if not pname or not price_txt:
            print("Missing product name or price.")
            return

        try:
            price = Decimal(price_txt)
        except ValueError:
            print("Price must be a number.")
            return

        # You already stored the current product id in self.pidf when you opened this editor
        pid = getattr(self, "pidf", None)
        if not pid:
            print("No product id to update.")
            return

        ok = self.db_manager.update_product(
            pid=pid,
            product_desc=pname,
            price=price,
            category_name=catused,
            sub_category=subused,
            vat = self.vatv,
            size="No Size",
            size_group="No Size",
        )

        if ok:
            print(f"Updated product id={pid}")
        else:
            print("Update failed.")

        # Go back and let the ProductPage refresh itself on show
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
        from productlist import ProductPage
        self.next_screenacc = ProductPage(self.username, self.rank)
        self.next_screenacc.show()
        self.hide()
    # Example methods to show how you’d swap widgets
    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    


