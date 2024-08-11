import psycopg2
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction import FeatureHasher
from sklearn.impute import SimpleImputer
from sklearn.ensemble import IsolationForest

# Path to the secrets
password_file_path = '/run/secrets/db-password'

# Read password
with open(password_file_path, 'r') as file:
    db_password = file.read().strip()

# Read query
with open('/app/etl/files/query-raw-access-data.sql') as sql_file:
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

# Extract columns
work_app_names = np.array([row[0] for row in query_results])
work_app_ids = np.array([str(row[1]) if row[1] is not None else 'missing' for row in query_results])
user_ids = np.array([str(row[3]) if row[3] is not None else 'missing' for row in query_results])
manager_ids = np.array([str(row[4]) if row[4] is not None else 'missing' for row in query_results])
type_of_work_ids = np.array([row[5] for row in query_results])
role_ids = np.array([row[6] for row in query_results])
users_group_ids = np.array([str(row[7]) if row[7] is not None else 'missing' for row in query_results])
permission_level_ids = np.array([str(row[8]) if row[8] is not None else 'missing' for row in query_results])
is_privileged = np.array([row[9] for row in query_results])

# Transform WorkAppNames with Label Encoding
label_encoder = LabelEncoder()
encoded_work_app_names = label_encoder.fit_transform(work_app_names)

# Transform UUIDs with Hash Encoding
hasher = FeatureHasher(n_features=10, input_type='string')

hashed_work_app_ids = hasher.transform([[uuid] for uuid in work_app_ids]).toarray()
hashed_user_ids = hasher.transform([[uuid] for uuid in user_ids]).toarray()
hashed_manager_ids = hasher.transform([[uuid] for uuid in manager_ids]).toarray()
hashed_users_group_ids = hasher.transform([[uuid] for uuid in users_group_ids]).toarray()
hashed_permission_level_ids = hasher.transform([[uuid] for uuid in permission_level_ids]).toarray()

# Transform is_priviliged into (-1, 0, 1)
# Replace None with -1
imputer = SimpleImputer(strategy='constant', fill_value=None)
imputed_is_privileged = imputer.fit_transform(is_privileged.reshape(-1, 1))
encoded_is_privileged = np.where(imputed_is_privileged == None, -1, imputed_is_privileged)
encoded_is_privileged = np.where(encoded_is_privileged == True, 1, encoded_is_privileged)
encoded_is_privileged = encoded_is_privileged.astype(int).ravel()

# Combine columns
transformed_data = np.hstack((
    encoded_work_app_names.reshape(-1, 1),
    hashed_work_app_ids,
    type_of_work_ids.reshape(-1, 1),
    role_ids.reshape(-1, 1),
    hashed_user_ids,
    hashed_manager_ids,
    hashed_users_group_ids,
    hashed_permission_level_ids,
    encoded_is_privileged.reshape(-1, 1)
))

# Save the data to be used by model
result_df = pd.DataFrame(transformed_data)
result_df.to_csv('/app/etl/files/data-model.csv', header=False, index=False)
print("Data Transformed and Saved successfully!")

while True:
    a = 0