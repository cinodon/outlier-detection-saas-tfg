from modules import data_processing as dp
from modules import db_processor as db


# Create a DB Processor
db_comm = db.DBProcessor()

# Connect DB
db_comm.db_connection()

# Create cursor
db_cursor = db_comm.db_create_cursor()

# Execute query
db_comm.execute_query()

# Get the results
query_results = db_comm.get_query_result()

# Close connection
db_comm.db_close()

# TRANSFORM DATA
sql_dataframe = dp.transform_data(query_results, db_cursor)

# Save the data to be used by model
dp.save_to_csv(sql_dataframe, '/app/etl/files/data-model.csv')