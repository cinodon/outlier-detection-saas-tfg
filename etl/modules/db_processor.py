import psycopg2

class DBProcessor:
    def __init__(self):
        # Path to the secrets
        self.password_file_path = '/run/secrets/db-password'
        # Path to sql_file
        self.sql_path = '/app/etl/files/query-raw-access-data.sql'
        # Conecction Settings
        self.db_config = {}
        self.conn = None

        self.cursor = None

    def db_connection(self):
        #Setup config
        self.set_db_config()

        # Connect to db
        self.conn = psycopg2.connect(**self.db_config)
        print("Connected successfully!")

    def set_db_config(self):
        db_password = self.db_read_pass()
        self.db_config = {
            'dbname': 'company148',
            'user': 'postgres',
            'password': db_password,
            'host': 'db',
            'port': '5432'
        }

    def db_read_pass(self):
        # Read password
        with open(self.password_file_path, 'r') as file:
            return file.read().strip()

    def db_create_cursor(self):
        self.cursor = self.conn.cursor()
        return self.cursor

    def execute_query(self):
        # Read query
        sql_query = self.read_sql_file()

        # Checks for cursor existence
        if self.cursor == None:
            self.db_create_cursor()

        # Execute query
        self.cursor.execute(sql_query)

    def read_sql_file(self):
        with open(self.sql_path) as sql_file:
            return sql_file.read()

    def get_query_result(self):
        return self.cursor.fetchall()

    def db_close(self):
        self.conn.close()
        self.cursor.close()