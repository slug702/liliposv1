import pymysql
import os
import subprocess
import platform
from datetime import datetime, timedelta, date
from decimal import Decimal
class DatabaseManager:

    def __init__(self):
        self.connection = self.connect_to_database()

    def connect_to_database(self):
        config_file = 'dbrs.txt'
        config = self.load_config(config_file)
        
        # Ensure that all necessary fields are present
        required_fields = ['host', 'user', 'password', 'database']
        for field in required_fields:
            if field not in config:
                print(f"Error: Missing '{field}' in the config file.")
                return None
        
        try:
            connection = pymysql.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                database=config['database'],
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Database connection successful!")
            return connection
        except pymysql.MySQLError as e:
            print(f"Error connecting to the database: {e}")
            return None
    def load_config(self, config_file):
        config = {}
        try:
            with open(config_file, 'r') as file:
                for line in file:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        config[key.strip()] = value.strip()
        except FileNotFoundError:
            print(f"Error: Config file '{config_file}' not found.")
        except Exception as e:
            print(f"Error reading config file: {e}")
        return config 
    
    def fetch_usernames(self):#get user names for login 
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT username FROM users")
                return [row['username'] for row in cursor.fetchall()]
        except pymysql.MySQLError as e:
            print(f"Error fetching usernames: {e}")
            return []
    def fetch_unpaid_invoice_ids(self):
        try:
            with self.connection.cursor() as cur:
                cur.execute("""
                    SELECT inv_id
                    FROM invoices
                    WHERE status IN ('UNPAID','NEW')
                    ORDER BY inv_id DESC
                """)
                rows = cur.fetchall()
                return [str(r['inv_id']) for r in rows]
        except pymysql.MySQLError as e:
            print(f"Error fetching invoices: {e}")
            return []
    def insert_invoice_new(self):
        """Create a blank invoice row with status NEW. Return the new inv_id."""
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "INSERT INTO invoices (status, order_date) VALUES ('NEW', NOW())"
                )
                new_id = cur.lastrowid
            self.connection.commit()
            return new_id
        except pymysql.MySQLError as e:
            print(f"insert_invoice_new error: {e}")
            self.connection.rollback()
            return None
    def verify_credentials(self, username, password): #verify login 
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
                result = cursor.fetchone()
                return result and result['password'] == password
        except pymysql.MySQLError as e:
            print(f"Error verifying credentials: {e}")
            return False
    def get_passlevel(self, username):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT position FROM users WHERE username = %s", (username,))
                result = cursor.fetchone()
                if result:
                    resultlevel = result['position']  # Assuming 'pass_rank' is a key in the returned dict
                    return resultlevel
                else:
                    return None
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            return None
    def fetch_categories_for_orders(self):
        sql = """
            SELECT DISTINCT TRIM(category_name) AS cat
            FROM products
            WHERE category_name IS NOT NULL AND TRIM(category_name) <> ''
            ORDER BY cat
        """
        try:
            with self.connection.cursor() as cur:   # DictCursor is set globally in your connect
                cur.execute(sql)
                rows = cur.fetchall()               # list of dicts like [{'cat': 'Mains'}, ...]
                
                # Build the category list
                categories = [r["cat"] for r in rows]
                
                # Always prepend "All"
                return ["All"] + categories

        except pymysql.MySQLError as e:
            print(f"Error fetching categories: {e}")
            return ["All"]   # fallback so UI doesn’t break
    #def fetch_all_products(self):
    #    try:
    #        with self.connection.cursor() as cursor:
    #            cursor.execute("SELECT `product_desc`, `price`, FROM products")
    #            return [(row['product_desc'], row['price']) for row in cursor.fetchall()]
    #    except pymysql.MySQLError as e:
    #        print(f"Error fetching products: {e}")
    #        return []
    # return full product rows (dicts)
    def fetch_all_products(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT pid, product_desc, price, size, size_group, vat
                    FROM products
                """)
                return cursor.fetchall()   # list of dicts
        except pymysql.MySQLError as e:
            print(f"Error fetching products: {e}")
            return []
    # simple insert of an item row into transactions
    def insert_transaction_item(self, inv_id, pid, desc, price, vat):
        try:
            with self.connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO transactions
                        (inv_id, p_id, tr_type, tr_desc, gross_price, vat, tr_date)
                    VALUES
                        (%s, %s, 'product', %s, %s, %s, NOW())
                """, (inv_id, pid, desc, price, vat))
            self.connection.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"insert_transaction_item error: {e}")
            self.connection.rollback()
            return False
    def fetch_transactions_for_invoice(self, inv_id: int):
        try:
            with self.connection.cursor() as cur:
                cur.execute("""
                    SELECT tr_id, tr_desc, gross_price, discount_rate
                    FROM transactions
                    WHERE inv_id = %s
                    ORDER BY tr_id
                """, (inv_id,))
                return cur.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error fetching transactions: {e}")
            return []
    def delete_transaction(self, tr_id: int) -> bool:
        try:
            with self.connection.cursor() as cur:
                cur.execute("DELETE FROM transactions WHERE tr_id = %s LIMIT 1", (tr_id,))
            self.connection.commit()
            return cur.rowcount == 1
        except pymysql.MySQLError as e:
            print(f"delete_transaction error: {e}")
            self.connection.rollback()
            return False    


    def fetch_subcategories_by_category(self, category_picked):
        try:
            with self.connection.cursor() as cursor:
                query = """
                    SELECT DISTINCT sub_category FROM products
                    WHERE category_name = %s AND sub_category IS NOT NULL
                """
                cursor.execute(query, (category_picked,))
                return [row['sub_category'] for row in cursor.fetchall()]
        except pymysql.MySQLError as e:
            print(f"Error fetching subcategories: {e}")
            return []
    def fetch_all_products_with_filter(self, category_picked):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT `product_desc`, `price` FROM products WHERE category_name = %s"
                cursor.execute(query, (category_picked,))
                return [(row['product_desc'], row['price']) for row in cursor.fetchall()]
        except pymysql.MySQLError as e:
            print(f"Error fetching products: {e}")
            return []

    def fetch_products_by_category_and_sub(self, category_picked, subcat):
        try:
            with self.connection.cursor() as cursor:
                if subcat == "All":
                    query = "SELECT product_desc, price FROM products WHERE category_name = %s"
                    cursor.execute(query, (category_picked,))
                else:
                    query = "SELECT product_desc, price FROM products WHERE category_name = %s AND sub_category = %s"
                    cursor.execute(query, (category_picked, subcat))
                return [(row['product_desc'], row['price']) for row in cursor.fetchall()]
        except pymysql.MySQLError as e:
            print(f"Error fetching products: {e}")
            return []

    
    def fetch_products_with_search(self, searchedfor):
        try:
            with self.connection.cursor() as cursor:
                query = """
                    SELECT product_desc, price
                    FROM products
                    WHERE product_desc LIKE %s
                """
                search_term = f"%{searchedfor}%"
                cursor.execute(query, (search_term,))
                return [(row['product_desc'], row['price']) for row in cursor.fetchall()]
        except pymysql.MySQLError as e:
            print(f"Error searching products: {e}")
            return []
    def fetch_product_list(self):
       
        sql = """
            SELECT
                pid,
                product_desc,
                price,
                category_name,
                sub_category,
                size,
                size_group
            FROM products
            ORDER BY product_desc
        """
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cur:
                cur.execute(sql)
                return cur.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error fetching products: {e}")
            return []
    def insert_product(self, product_desc, price, category_name, sub_category, vat,
                   size="No Size", size_group="No Size"):
        
        try:
            with self.connection.cursor() as cur:
                sql = """
                    INSERT INTO products
                        (product_desc, price, category_name, sub_category, vat, size, size_group)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(sql, (
                    product_desc,
                    price,
                    (category_name or None),
                    (sub_category or None),
                    vat,
                    size,
                    size_group,
                ))
                new_id = cur.lastrowid
            self.connection.commit()
            return new_id
        except pymysql.MySQLError as e:
            print(f"insert_product error: {e}")
            self.connection.rollback()
            return None
    def delete_product(self, pid: int) -> bool:
        """Delete one product by pid. Returns True if a row was deleted."""
        try:
            with self.connection.cursor() as cur:
                cur.execute("DELETE FROM products WHERE pid = %s", (pid,))
            self.connection.commit()
            return cur.rowcount > 0
        except pymysql.MySQLError as e:
            print(f"delete_product error: {e}")
            self.connection.rollback()
            return False
    def update_product(self, pid, product_desc, price, category_name, sub_category, vat, size, size_group):
       
        sql = """
            UPDATE products
            SET product_desc = %s,
                price        = %s,
                category_name= %s,
                sub_category = %s,
                vat = %s,
                size         = %s,
                size_group   = %s
            WHERE pid = %s
            LIMIT 1
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(sql, (
                    product_desc, price, category_name, sub_category, vat, size, size_group, pid
                ))
            self.connection.commit()
            return cur.rowcount == 1
        except Exception as e:
            print(f"update_product error: {e}")
            return False
    