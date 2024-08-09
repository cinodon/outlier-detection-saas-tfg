import psycopg2

# Path to the secrets
password_file_path = '/run/secrets/db-password'

# Read password
with open(password_file_path, 'r') as file:
    db_password = file.read().strip()

# Connection Settings
db_config = {
    'dbname': 'company148',
    'user': 'postgres',
    'password': db_password,
    'host': 'db',
    'port': '5432'
}

# Connect to database
conn = psycopg2.connect(**db_config)
print("Connected successfully!")