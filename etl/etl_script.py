import yaml
from modules import data_processing as dp
from modules import db_processor as db
from modules import clustering_models as cm

sql_input_data = './files/sql/query-raw-access-data.sql'
sql_output_data = './files/sql/query-output-model-data.sql'

# Config
with open("./config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Read from config
connect_database = config['connect_database']

# Connect to database, execute queries, transform data...
if connect_database:
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
    dp.save_to_csv(sql_dataframe, './files/input/model-input-data.csv')
    dp.save_to_csv(output_dataframe, './files/output/output-base.csv')


# -MODELS-
# Load CSV for Models
model_input_df = dp.load_csv('./files/input/model-input-data.csv')

# Excluir columnas
excluded_columns = config.get('excluded_columns', {})
model_input_df = dp.exclude_columns(model_input_df, excluded_columns)

input_df_scaled = cm.scale_data(model_input_df)
if connect_database == False:
    output_dataframe = dp.load_csv('./files/output/output-base.csv')

# Select Model 0 - Isolation Forest | 1 - LoF | 2 - DBSCAN | 3 - OPTICS
# Set Isolation Forest Parameters range
n_estimators = config['n_estimators']
max_samples = config['max_samples']
contamination = config['contamination']
run_if = config['run_if']
if run_if:
    for ne in n_estimators:
        for ms in max_samples:
            for c in contamination:
                # Execute model
                output_dataframe['anomaly_score'] = cm.execute_isolation(input_df_scaled, ne, ms, c)

                # Save data
                output_file = f'./files/output/IF/data/IF-ne{ne}-ms{ms}-c{c}.csv'
                dp.save_to_csv(output_dataframe, output_file)

# Set DBSCAN Parameters range
eps = config['eps']
min_samples = config['min_samples']
run_dbscan = config['run_dbscan']
if run_dbscan:
    for e in eps:
        for ms in min_samples:
            # Execute model
            output_dataframe['anomaly_score'] = cm.execute_dbscan(input_df_scaled, e, ms)

            # Save data
            output_file = f'./files/output/DBSCAN/data/DBSCAN-eps{e}-ms{ms}.csv'
            dp.save_to_csv(output_dataframe, output_file)


# Local Outlier Factor
n_neighbors = [5, 10, 20]
run_lof = config['run_lof']
if run_lof:
    for n in n_neighbors:
        # Execute model
        output_dataframe['anomaly_score'] = cm.execute_lof(input_df_scaled, n)

        # Save data
        output_file = f'./files/output/LOF/data/LOF-n{n}.csv'
        dp.save_to_csv(output_dataframe, output_file)
