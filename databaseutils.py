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
                    resultlevel = result['']  # Assuming 'pass_rank' is a key in the returned dict
                    return resultlevel
                else:
                    return None
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            return None