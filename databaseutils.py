import pymysql
import os
import subprocess
import platform
from datetime import datetime, timedelta, date
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
    def fetch_categories_for_orders(self):#get districts for main window
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT category_name FROM categories")
                return [row['category_name'] for row in cursor.fetchall()]
        except pymysql.MySQLError as e:
            print(f"Error fetching categories: {e}")
            return []
    def fetch_all_products(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT `product_desc`, `price` FROM products")
                return [(row['product_desc'], row['price']) for row in cursor.fetchall()]
        except pymysql.MySQLError as e:
            print(f"Error fetching products: {e}")
            return []
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