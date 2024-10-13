import psycopg2
import os

class DBProcessor:
    def __init__(self):
        # Path to the secrets
        self.password_file_path = os.getenv('DB_PASSWORD_FILE', '../database/db-password')

        # Conecction Settings
        self.db_config = {}
        self.conn = None

        self.cursor = None

    def db_connection(self, db_config):
        #Setup config
        self.set_db_config(db_config)

        # Connect to db
        self.conn = psycopg2.connect(**self.db_config)
        print("Connected successfully!")

    def set_db_config(self, db_config):
        db_password = self.db_read_pass()
        db_config['password'] = db_password
        self.db_config = db_config


    def db_read_pass(self):
        # Read password
        with open(self.password_file_path, 'r') as file:
            return file.read().strip()

    def db_create_cursor(self):
        self.cursor = self.conn.cursor()
        return self.cursor

    def execute_query(self, sql_path):
        # Read query
        sql_query = self.read_sql_file(sql_path)

        # Checks for cursor existence
        if self.cursor == None:
            self.db_create_cursor()

        # Execute query
        self.cursor.execute(sql_query)

    def read_sql_file(self, sql_path):
        with open(sql_path) as sql_file:
            return sql_file.read()

    def get_query_result(self):
        return self.cursor.fetchall()

    def db_close(self):
        self.conn.close()
        self.cursor.close()

