import yaml
from modules import data_processing as dp
from modules import db_processor as db
from modules import clustering_models as cm
from modules import plot_management as pm

# Config
with open("./etl_config.yaml", "r") as f:
    config = yaml.safe_load(f)

sql_input_data = config['sql_input_data']
sql_output_data = config['sql_output_data']

# Read from config
connect_database = config['connect_database']

# Connect to database, execute queries, transform data...
if connect_database:
    # Create a DB Processor
    db_comm = db.DBProcessor()

    # Connect DB
    db_config = config['db_config']
    db_comm.db_connection(db_config)

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

# Normalize
input_df_scaled = cm.scale_data(model_input_df)

if connect_database == False:
    output_dataframe = dp.load_csv('./files/output/output-base.csv')

# Reduce dimensionality
plot_df = dp.pca_reduce_dimensions(input_df_scaled)

# Select Model 0 - Isolation Forest | 1 - LoF | 2 - DBSCAN | 3 - OPTICS
# Set Isolation Forest Parameters range
n_estimators = config['n_estimators']
max_samples = config['max_samples']
contamination = config['contamination']
run_if = config['run_if']
if_save_data = config['if_save_data']
if_save_plot = config['if_save_plot']
if run_if:
    for ne in n_estimators:
        for ms in max_samples:
            for c in contamination:
                # Execute model
                output_dataframe['anomaly_score'] = cm.execute_isolation(input_df_scaled, ne, ms, c)

                # Get percentage of outliers
                num_anomalies = (output_dataframe['anomaly_score'] == -1).sum()
                total_entries = len(output_dataframe)
                percentage_anomalies = (num_anomalies / total_entries) * 100

                # Print percentage
                print(f'For IF with n_estimators {ne}, max_samples {ms}, contamintation {c}: {percentage_anomalies:.2f}%')

                # Save data
                if if_save_data:
                    output_file = f'./files/output/IF/data/IF-ne{ne}-ms{ms}-c{c}.csv'
                    dp.save_to_csv(output_dataframe, output_file)

                if if_save_plot:
                    # Add column
                    plot_df['anomaly_score'] = output_dataframe['anomaly_score']

                    # Create and save plot
                    output_image = f'./files/output/IF/image/IF-ne{ne}-ms{ms}-c{c}.png'
                    pm.get_plot(f'Isolation Forest\nn_estimators={ne}-max_samples={ms}-contamination={c}',
                                plot_df,
                                output_image)


# Set DBSCAN Parameters range
eps = config['eps']
min_samples = config['min_samples']
run_dbscan = config['run_dbscan']
dbscan_save_data = config['dbscan_save_data']
dbscan_save_plot = config['dbscan_save_plot']
if run_dbscan:
    for e in eps:
        for ms in min_samples:
            # Execute model
            output_dataframe['anomaly_score'] = cm.execute_dbscan(input_df_scaled, e, ms)

            # Get percentage of outliers
            num_anomalies = (output_dataframe['anomaly_score'] == -1).sum()
            total_entries = len(output_dataframe)
            percentage_anomalies = (num_anomalies / total_entries) * 100

            # Print percentage
            print(f'For DBSCAN with eps {e}, min_samples {ms}: {percentage_anomalies:.2f}%')

            # Save data
            if dbscan_save_data:
                output_file = f'./files/output/DBSCAN/data/DBSCAN-eps{e}-ms{ms}.csv'
                dp.save_to_csv(output_dataframe, output_file)

            # Save plot
            if dbscan_save_plot:
                # Add column
                plot_df['anomaly_score'] = output_dataframe['anomaly_score']

                # Create and save plot
                output_image = f'./files/output/DBSCAN/image/DBSCAN-e{ne}-ms{ms}.png'
                pm.get_plot(f'DBSCAN\neps={ne}-min_samples={ms}',
                            plot_df,
                            output_image)






# Local Outlier Factor
n_neighbors = [5, 10, 20]
run_lof = config['run_lof']
lof_save_data = config['lof_save_data']
lof_save_plot = config['lof_save_plot']
if run_lof:
    for n in n_neighbors:
        # Execute model
        output_dataframe['anomaly_score'] = cm.execute_lof(input_df_scaled, n)

        # Get percentage of outliers
        num_anomalies = (output_dataframe['anomaly_score'] == -1).sum()
        total_entries = len(output_dataframe)
        percentage_anomalies = (num_anomalies / total_entries) * 100

        # Print percentage
        print(f'For LOF with n_neighbors {n}: {percentage_anomalies:.2f}%')

        # Save data
        if lof_save_data:
            output_file = f'./files/output/LOF/data/LOF-n{n}.csv'
            dp.save_to_csv(output_dataframe, output_file)

        # Save plot
        if lof_save_plot:
            # Add column
            plot_df['anomaly_score'] = output_dataframe['anomaly_score']

            # Create and save plot
            output_image = f'./files/output/LOF/image/LOF-n{n}.png'
            pm.get_plot(f'LOF\nn_neighbors={n}',
                        plot_df,
                        output_image)
