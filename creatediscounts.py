# creatediscounts.py
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QCheckBox
)
from decimal import Decimal
from databaseutils import DatabaseManager

class CreateDiscounts(QWidget):
    """
    Per-product discount page.
    Accepts tr_id from saleslandingpage and lets you:
      - enter a discount rate
      - Calculate Discount (preview only)
      - Place Discount (persist)
    Shows: Gross price, Net price, VAT total (before),
           Net before discount, Net after discount, Gross after discount.
    """
    def __init__(self, username, rank, tr_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Per-Product Discount")
        self.username = username
        self.rank = rank
        self.tr_id = tr_id
        self.db = DatabaseManager()
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
        self.label_style = "font-size: 24px; font-weight: bold; font-family: 'Segoe UI'; margin-bottom: 10px"
        self.line_style = """
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
        """
        
        self.VAT_RATE = Decimal("0.12")

        # --- UI ---
        self.goback = QPushButton("Go Back")
        
        self.lbl_title = QLabel(f"Apply Discount to Transaction ID: {tr_id}")
        self.lbl_gross = QLabel("Gross price: —")
        self.lbl_net = QLabel("Net price: —")
        self.lbl_vat = QLabel("VAT total: —")

        self.discount_rate = QLineEdit()
        self.discount_rate.setPlaceholderText("Discount rate")

        self.btn_calc = QPushButton("Calculate Discount")
        self.btn_place = QPushButton("Place Discount")

        self.lbl_net_before = QLabel("Net before discount: —")
        self.lbl_net_after = QLabel("Net after discount: —")
        self.lbl_gross_after = QLabel("Gross after discount: —")

        top = QVBoxLayout(self)
        top.addWidget(self.goback)
        top.addWidget(self.lbl_title)
       
        row1 = QHBoxLayout()
     
        row1.addWidget(self.lbl_gross)
        row1.addWidget(self.lbl_net)
        row1.addWidget(self.lbl_vat)
        top.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(self.discount_rate)
        row2.addWidget(self.btn_calc)
        row2.addWidget(self.btn_place)
        top.addLayout(row2)

        top.addWidget(self.lbl_net_before)
        top.addWidget(self.lbl_net_after)
        top.addWidget(self.lbl_gross_after)

        # Load the transaction and populate labels
        self._load_tr()

        # Wire buttons
        self.btn_calc.clicked.connect(self.calculate_discount_preview)
        self.btn_place.clicked.connect(self.place_discount_commit)
        self.goback.clicked.connect(self.gobacktosales)
        for line_edits in [self.discount_rate]:
            line_edits.setStyleSheet(self.label_style)
        for lbl in [self.lbl_title, self.lbl_gross, self.lbl_net, self.lbl_vat, self.lbl_gross_after, self.lbl_net_after, self.lbl_net_before]:
            lbl.setStyleSheet(self.label_style)
        for btn in [self.btn_calc, self.btn_place, self.goback]:
            btn.setStyleSheet(self.button_style)

    # --- Data load helpers ---
    def gobacktosales(self):
        from saleslandingpage import POSHomePage
        self.next_screenacc = POSHomePage(self.username, self.rank)
        self.next_screenacc.show()
        self.hide()
    def _load_tr(self):
        """
        Fetch the transaction line by tr_id.
        Expecting columns at minimum:
          - gross_price (VAT-inclusive sticker)
          - vat ("yes"/"no")
          - discount_rate (line-level, may be NULL/0)
          - total_discount (line-level, may be NULL/0)
          - net, vat_total (already stored)
        """
        row = self.db.fetch_transaction_by_id(self.tr_id)  # You likely have/ can add this simple DAO
        if not row:
            self.lbl_title.setText(f"Transaction not found: {self.tr_id}")
            return

        self.vat_flag = (str(row.get("vat","yes")).strip().lower() == "yes")
        self.gross = Decimal(str(row.get("gross_price", "0")))
        self.stored_net = Decimal(str(row.get("net", "0")))
        self.stored_vat = Decimal(str(row.get("vat_total", "0")))
        self.line_disc_rate = Decimal(str(row.get("discount_rate") or "0"))
        self.line_disc_total = Decimal(str(row.get("total_discount") or "0"))

        # Top labels from stored values (or recompute if needed)
        if self.stored_net == 0 and self.gross > 0:
            rate = self.VAT_RATE if self.vat_flag else Decimal("0")
            self.stored_net = round(self.gross / (Decimal("1.00")+rate), 2) if rate>0 else round(self.gross,2)
            self.stored_vat = round(self.gross - self.stored_net, 2)

        self._refresh_top_labels()

        # Seed discount_rate input with any existing line rate
        if self.line_disc_rate != 0:
            self.discount_rate.setText(str(self.line_disc_rate))

    def _refresh_top_labels(self):
        self.lbl_gross.setText(f"Gross price: ₱{self.gross:.2f}")
        self.lbl_net.setText(f"Net price: ₱{self.stored_net:.2f}")
        self.lbl_vat.setText(f"VAT total: ₱{self.stored_vat:.2f}")

    # --- Button logic ---
    def calculate_discount_preview(self):
        if self.gross is None:
            return
        rate = self.VAT_RATE if self.vat_flag else Decimal("0.00")

        net_before = round(self.gross / (Decimal("1.00")+rate), 2) if rate>0 else round(self.gross, 2)

        # read entered discount rate (fraction)
        try:
            d_rate = Decimal(self.discount_rate.text().strip() or "0")
            d_ratef = d_rate/100 
        except Exception:
            d_ratef = Decimal("0")

        line_disc = round(net_before * d_ratef, 2)
        net_after = round(net_before - line_disc, 2)
        vat_total = round(net_after * rate, 2)
        gross_after = round(net_after + vat_total, 2)

        self.lbl_net_before.setText(f"Net before discount: ₱{net_before:.2f}")
        self.lbl_net_after.setText(f"Net after discount: ₱{net_after:.2f}")
        self.lbl_gross_after.setText(f"Gross after discount: ₱{gross_after:.2f}")

        # stash for commit
        self._preview = {
            "discount_rate": d_ratef,
            "total_discount": line_disc,
            "net": net_after,
            "vat_total": vat_total,
            "gross": gross_after
        }
    def discount_placed(self):
        from saleslandingpage import POSHomePage
        self.next_screenacc = POSHomePage(self.username, self.rank)
        self.next_screenacc.show()
        self.hide()

    def place_discount_commit(self):
        """
        Persist line-level discount to this transaction row.
        Keeps product-level discount in `total_discount`/`discount_rate`,
        and updates net/vat_total/gross_price accordingly.
        """
        # Ensure preview has been run at least once
        if not hasattr(self, "_preview"):
            self.calculate_discount_preview()

        d = self._preview

        ok = self.db.update_transaction_discount_line(
            tr_id=self.tr_id,
            discount_rate=str(d["discount_rate"]),
            total_discount=str(d["total_discount"]),
            net=str(d["net"]),
            vat_total=str(d["vat_total"]),
            gross_price=str(d["gross"]),
        )

        if ok:
            self.lbl_title.setText(f"Saved discount to tr_id {self.tr_id}.")
            self.discount_placed()
        else:
            self.lbl_title.setText(f"Failed to save discount for tr_id {self.tr_id}.")
