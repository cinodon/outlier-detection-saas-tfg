import psycopg2

# Path to the secrets
password_file_path = '../database/db-password'

# Read password
with open(password_file_path, 'r') as file:
    db_password = file.read().strip()

# Conecction Settings
db_config = {
    'dbname': 'company148',
    'user': 'postgres',
    'password': db_password,
    'host': 'localhost',
    'port': '5432'
}

# Connect to database
conn = psycopg2.connect(**db_config)
print("Connected successfully!")

