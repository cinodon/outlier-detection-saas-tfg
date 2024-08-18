from datetime import datetime

from modules import data_processing as dp
from modules import db_processor as db
from modules import clustering_models as cm

sql_input_data = '/app/etl/files/sql/query-raw-access-data.sql'
sql_output_data = '/app/etl/files/sql/query-output-model-data.sql'


# Create a DB Processor
db_comm = db.DBProcessor()

# Connect DB
db_comm.db_connection()

# Create cursor
db_cursor = db_comm.db_create_cursor()

# Execute query INPUT
db_comm.execute_query(sql_input_data)

# Get the results INPUT
query_results = db_comm.get_query_result()

# TRANSFORM DATA for input model
sql_dataframe = dp.transform_query_data(query_results, db_cursor)

# Execute output query
db_comm.execute_query(sql_output_data)

# Get the results
output_query_results = db_comm.get_query_result()

# Transform output to dataframe
output_dataframe = dp.transform_query_to_dataframe(output_query_results, db_cursor)

# Close connection
db_comm.db_close()

# Save the data to be used by model
dp.save_to_csv(sql_dataframe, '/app/etl/files/input/model-input-data.csv')


# -MODELS-
# Load CSV for Models
model_input_df = dp.load_model_input('/app/etl/files/input/model-input-data.csv')
input_df_scaled = cm.scale_data(model_input_df)

# Select Model 0 - Isolation Forest | 1 - LoF | 2 - DBSCAN | 3 - OPTICS
# Set Isolation Forest Parameters range
n_estimators = [500]
max_samples = [0.8, 0.9, 1.0]

for ne in n_estimators:
    for ms in max_samples:
        # Execute model
        output_dataframe['anomaly_score'] = cm.execute_isolation(input_df_scaled, ne, ms)

        # Save data
        output_file = f'/app/etl/files/output/IF/data/IF-ne{ne}-ms{ms}-cAuto.csv'
        dp.save_to_csv(output_dataframe, output_file)

# Set DBSCAN Parameters range
eps = [0.6]
min_samples = [5]

for e in eps:
    for ms in min_samples:
        # Execute model
        output_dataframe['anomaly_score'] = cm.execute_dbscan(input_df_scaled, e, ms)

        # Save data
        output_file = f'/app/etl/files/output/DBSCAN/data/DBSCAN-eps{e}-ms{ms}.csv'
        dp.save_to_csv(output_dataframe, output_file)


# Local Outlier Factor
n_neighbors = [5, 10, 20]
for n in n_neighbors:
    # Execute model
    output_dataframe['anomaly_score'] = cm.execute_lof(input_df_scaled, n)

    # Save data
    output_file = f'/app/etl/files/output/LOF/data/LOF-n{n}.csv'
    dp.save_to_csv(output_dataframe, output_file)
