from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QCheckBox, QMessageBox
)
from decimal import Decimal
from databaseutils import DatabaseManager

VAT = Decimal("0.12")

class InvoicePayment(QWidget):
    """
    Simple Payment Summary screen:
      - Shows totals (vatable, nonvatable, vat, discounts)
      - Apply cart-level discount
      - Select Mode of Payment
      - Save invoice footer totals
    """
    def __init__(self, username, rank, inv_id, parent=None):
        super().__init__(parent)
        self.username = username
        self.rank = rank
        self.inv_id = inv_id
        self.db = DatabaseManager()
        self.setWindowTitle(f"Invoice Payment — #{inv_id}")

        # rows need vat flag, net, total_discount
        # invoicepayment.py  __init__
        self.rows = self.db.fetch_invoice_lines_for_payment(int(inv_id)) or []

        self.cart_disc_type = None
        self.cart_disc_value = Decimal("0.00")

        # --- UI labels
        self.goback = QPushButton("Go Back")
        self.goback.clicked.connect(self.gobacktosales)
        self.lbl_vatable_sales  = QLabel("VATable Sales: ₱0.00")
        self.lbl_exempt_sales   = QLabel("Non-VAT Sales: ₱0.00")
        self.lbl_line_discounts = QLabel("Line Discounts: ₱0.00")
        self.lbl_cart_discount  = QLabel("Cart Discount: ₱0.00")
        self.lbl_total_discount = QLabel("Total Discount: ₱0.00")
        self.lbl_total_vat      = QLabel("VAT (12%): ₱0.00")
        self.lbl_final_amount   = QLabel("<b>Amount Payable: ₱0.00</b>")

        # --- cart discount inputs
        self.cmb_disc_type = QComboBox(); self.cmb_disc_type.addItems(["%"])
        self.txt_disc_val  = QLineEdit(); self.txt_disc_val.setPlaceholderText("10 or 100")
        self.btn_disc      = QPushButton("Apply Cart Discount")
        self.btn_disc.clicked.connect(self.apply_cart_discount)

        # --- payment
        self.cmb_mop = QComboBox(); self.cmb_mop.addItems(["Cash", "GCash", "Credit Card", "Debit"])
        self.txt_paid = QLineEdit(); self.txt_paid.setPlaceholderText("Amount Paid")
        self.lbl_change = QLabel("Change: ₱0.00")
        self.btn_confirm = QPushButton("Confirm Payment")
        self.txt_paid.textEdited.connect(self.update_change)
        self.btn_confirm.clicked.connect(self.save_invoice)
        # --- VAT toggle
        self.chk_vat = QCheckBox("Apply VAT")
        self.chk_vat.setChecked(True)
        self.chk_vat.stateChanged.connect(self.recompute)

        # --- layout
        root = QVBoxLayout(self)
        root.addWidget(self.goback)
        root.addWidget(self.lbl_vatable_sales)
        root.addWidget(self.lbl_exempt_sales)
        root.addWidget(self.lbl_line_discounts)

        row = QHBoxLayout()
        row.addWidget(self.lbl_cart_discount)
        row.addWidget(self.cmb_disc_type)
        row.addWidget(self.txt_disc_val)
        row.addWidget(self.btn_disc)
        root.addLayout(row)

        root.addWidget(self.lbl_total_discount)
        root.addWidget(self.lbl_total_vat)
        root.addWidget(self.lbl_final_amount)
        root.addWidget(self.chk_vat)

        payrow = QHBoxLayout()
        payrow.addWidget(QLabel("MOP:")); payrow.addWidget(self.cmb_mop)
        root.addLayout(payrow)

        pay2 = QHBoxLayout()
        pay2.addWidget(QLabel("Paid:")); pay2.addWidget(self.txt_paid)
        pay2.addWidget(self.lbl_change)
        root.addLayout(pay2)

        root.addWidget(self.btn_confirm)

        self.recompute()

    # --- logic
    def apply_cart_discount(self):
        raw = self.txt_disc_val.text().strip() or "0"
        try:
            val = Decimal(raw)
        except:
            val = Decimal("0")
        self.cart_disc_type = "PCT" if self.cmb_disc_type.currentText() == "%" else "ABS"
        self.cart_disc_value = (val/Decimal("100")) if self.cart_disc_type=="PCT" else val
        self.recompute()

    def recompute(self):
        # 1) Gather bases (these are VAT-EXCLUSIVE "net" amounts from rows)
        vatable_base = sum(Decimal(str(r["net"])) for r in self.rows
                        if str(r.get("vat", "yes")).lower() == "yes")
        exempt_base  = sum(Decimal(str(r["net"])) for r in self.rows
                        if str(r.get("vat", "yes")).lower() != "yes")
        line_discounts = sum(Decimal(str(r.get("total_discount", 0))) for r in self.rows)

        base_total = (vatable_base + exempt_base)

        # 2) Compute cart discount amount
        if self.cart_disc_type == "PCT":
            cart_disc_total = (self.cart_disc_value * base_total).quantize(Decimal("0.01"))
            # split by share of base
            v_share = (vatable_base / base_total) if base_total > 0 else Decimal("0")
            e_share = Decimal("1") - v_share
            cart_disc_v = (cart_disc_total * v_share).quantize(Decimal("0.01"))
            cart_disc_e = cart_disc_total - cart_disc_v
        elif self.cart_disc_type == "ABS":
            cart_disc_total = min(base_total, self.cart_disc_value).quantize(Decimal("0.01"))
            v_share = (vatable_base / base_total) if base_total > 0 else Decimal("0")
            cart_disc_v = (cart_disc_total * v_share).quantize(Decimal("0.01"))
            cart_disc_e = cart_disc_total - cart_disc_v
        else:
            cart_disc_total = Decimal("0.00")
            cart_disc_v = Decimal("0.00")
            cart_disc_e = Decimal("0.00")

        # 3) Discounted bases (still VAT-EXCLUSIVE here)
        vatable_after_base = (vatable_base - cart_disc_v).quantize(Decimal("0.01"))
        exempt_after_base  = (exempt_base  - cart_disc_e).quantize(Decimal("0.01"))

        # 4) VAT = 12% of the discounted VATable *base* (exclusive of VAT)
        # 4) VAT only if checkbox is checked
        if self.chk_vat.isChecked():
            vat_amount = (vatable_after_base * VAT).quantize(Decimal("0.01"))
        else:
            vat_amount = Decimal("0.00")


        # 5) Final payable = discounted bases + VAT on VATable base
        subtotal_ex_vat = (vatable_after_base + exempt_after_base).quantize(Decimal("0.01"))
        final_amount = (subtotal_ex_vat + vat_amount).quantize(Decimal("0.01"))

        total_discount = (line_discounts + cart_disc_total).quantize(Decimal("0.01"))

        # 6) Update UI — show bases (exclusive of VAT) for the sales lines
        self.lbl_vatable_sales.setText(f"VATable Sales: ₱{vatable_after_base:.2f}")
        self.lbl_exempt_sales.setText(f"Non-VAT Sales: ₱{exempt_after_base:.2f}")
        self.lbl_line_discounts.setText(f"Line Discounts: ₱{line_discounts:.2f}")
        self.lbl_cart_discount.setText(f"Cart Discount: ₱{cart_disc_total:.2f}")
        self.lbl_total_discount.setText(f"Total Discount: ₱{total_discount:.2f}")
        self.lbl_total_vat.setText(f"VAT (12%): ₱{vat_amount:.2f}")
        self.lbl_final_amount.setText(f"<b>Amount Payable: ₱{final_amount:.2f}</b>")

        # footer numbers to persist
        self.footer = dict(
            vatable_total=vatable_after_base,     # base, excl. VAT
            nonvatable_total=exempt_after_base,   # base, excl. VAT
            total_vat=vat_amount,
            cart_discount=cart_disc_total,
            total_discount=total_discount,
            final_amount_to_pay=final_amount,
            status = "PAID"
        )
        self.update_change()

    def update_change(self):
        try:
            paid = Decimal(self.txt_paid.text().strip() or "0")
        except:
            paid = Decimal("0")

        due = self.footer["final_amount_to_pay"] if hasattr(self, "footer") else Decimal("0")

        mop = self.cmb_mop.currentText()
        if mop != "Cash":
            # force paid = due
            paid = due
            self.txt_paid.setText(f"{due:.2f}")   # lock the input to exact payable
            change = Decimal("0.00")
        else:
            # normal cash behavior
            change = (paid - due).quantize(Decimal("0.01"))
            if change < 0:
                change = Decimal("0.00")

        self.lbl_change.setText(f"Change: ₱{change:.2f}")
        self._paid_amount = paid  # cache actual paid


    def save_invoice(self):
        if not hasattr(self, "footer"):
            return

        mop = self.cmb_mop.currentText()
        due = self.footer["final_amount_to_pay"]

        paid = getattr(self, "_paid_amount", due)

        # reject non-cash overpayments
        if mop != "Cash" and paid != due:
            QMessageBox.warning(self, "Invalid Payment", "Non-cash payments must equal amount payable.")
            return

        # write invoice footer + insert payment/change lines...
        self.db.update_invoice_totals(
            self.inv_id,
            str(self.footer["vatable_total"]),
            str(self.footer["nonvatable_total"]),
            str(self.footer["total_vat"]),
            str(self.footer["cart_discount"]),
            str(self.footer["total_discount"]),
            str(self.footer["final_amount_to_pay"]),
            str(self.footer["status"]),
            mop
        )

        # always insert payment line = paid
        self.db.insert_payment_line(int(self.inv_id), mop, str(paid.quantize(Decimal("0.01"))))

        # only insert change line if mop == Cash and change > 0
        change = paid - due
        if mop == "Cash" and change > 0:
            self.db.insert_change_line(int(self.inv_id), str(change.quantize(Decimal("0.01"))))
        
        QMessageBox.information(self, "Saved", "Invoice updated and payment recorded.")
        self.gobacktosales()
        self.close()
        


    def gobacktosales(self):
        from saleslandingpage import POSHomePage
        self.next_screenacc = POSHomePage(self.username, self.rank)
        self.next_screenacc.show()
        self.hide()