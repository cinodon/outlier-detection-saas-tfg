import psycopg2

# Path to the secrets
password_file_path = '/run/secrets/db-password'

# Read password
with open(password_file_path, 'r') as file:
    db_password = file.read().strip()

# Read query
with open('/files/query-raw-access-data.sql') as sql_file:
    sql_query = sql_file.read()

# Conecction Settings
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

# Create cursor
cursor = conn.cursor()
cursor.execute(sql_query)

# Get the results
query_results = cursor.fetchall()

# Close connection
cursor.close()
conn.close()

