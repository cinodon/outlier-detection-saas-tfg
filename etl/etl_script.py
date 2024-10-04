import yaml
from modules import data_processing as dp
from modules import db_processor as db
from modules import clustering_models as cm
from modules import plot_management as pm

def get_common_outliers():
    # Get common outliers
    if_output = dp.load_csv('./files/output/IF/data/IF-ne500-ms0.9-c0.05.csv')
    dbscan_output = dp.load_csv('./files/output/DBSCAN/data/DBSCAN-eps1.7-ms4.csv')
    lof_output = dp.load_csv('./files/output/LOF/data/LOF-n10.csv')

    # Merge outliers
    common_outliers = dp.get_common_outliers(if_output, dbscan_output)
    common_outliers = dp.get_common_outliers(common_outliers, lof_output)

    # Save file
    dp.save_to_csv(common_outliers, './files/output/common_outliers.csv')

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

# Exclude columns
excluded_columns = config.get('excluded_columns', {})
model_input_df = dp.exclude_columns(model_input_df, excluded_columns)

# Normalize
input_df_scaled = cm.scale_data(model_input_df)

# Reduce dimensionality
if_save_plot = config['if_save_plot']
dbscan_save_plot = config['dbscan_save_plot']
lof_save_plot = config['lof_save_plot']
if if_save_plot or dbscan_save_plot or lof_save_plot:
    input_df_plot = dp.tsne_reduce_to_3D(input_df_scaled)

# Get base output file
if not connect_database:
    output_dataframe = dp.load_csv('./files/output/output-base.csv')



# Select Model 0 - Isolation Forest | 1 - LoF | 2 - DBSCAN
# Set Isolation Forest Parameters range
n_estimators = config['n_estimators']
max_samples = config['max_samples']
contamination = config['contamination']
max_features = config['max_features']
bootstrap = config['bootstrap']
run_if = config['run_if']
if_save_data = config['if_save_data']
if_save_plot = config['if_save_plot']
if run_if:
    for ne in n_estimators:
        for ms in max_samples:
            for c in contamination:
                for mf in max_features:
                    for b in bootstrap:
                        # Execute model
                        output_dataframe['anomaly_score'] = cm.execute_isolation(input_df_scaled, ne, ms, c, mf, b)

                        # Get percentage of outliers
                        num_anomalies = (output_dataframe['anomaly_score'] == -1).sum()
                        total_entries = len(output_dataframe)
                        percentage_anomalies = (num_anomalies / total_entries) * 100

                        # Print percentage
                        print(f'For IF with n_estimators {ne}, max_samples {ms}, contamination {c}: {percentage_anomalies:.2f}%')

                        # Save data
                        if if_save_data:
                            output_file = f'./files/output/IF/data/IF-ne{ne}-ms{ms}-c{c}.csv'
                            dp.save_to_csv(output_dataframe, output_file)

                        # Save plot
                        if if_save_plot:
                            # Transform to dataframe and add column 'anomaly_score'
                            df_plot = dp.transform_to_dataframe(input_df_plot, ['VAR1', 'VAR2', 'VAR3'])
                            df_plot['anomaly_score'] = output_dataframe['anomaly_score']

                            # Plot
                            pm.get_plot3D(f'Isolation Forest\nn_estimators={ne}-max_samples={ms}-cont.{c}-%={percentage_anomalies:.2f}', df_plot,
                                        f'./files/output/IF/images/IF-ne{ne}-ms{ms}-cont{c}.png')


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
                # Transform to dataframe and add column 'anomaly_score'
                df_plot = dp.transform_to_dataframe(input_df_plot, ['VAR1', 'VAR2', 'VAR3'])
                # Transform clusters ID to inliers = 1
                output_dataframe['anomaly_score'] = dp.clusters_to_inliers(output_dataframe['anomaly_score'])
                df_plot['anomaly_score'] = output_dataframe['anomaly_score']

                # Plot
                pm.get_plot3D(f'DBSCAN\neps={e}-min_samples={ms}-%={percentage_anomalies:.2f}', df_plot,
                              f'./files/output/DBSCAN/images/DBSCAN-eps{e}-ms{ms}.png')


# Local Outlier Factor
run_lof = config['run_lof']
n_neighbors = config['n_neighbors']
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
            # Transform to dataframe and add column 'anomaly_score'
            df_plot = dp.transform_to_dataframe(input_df_plot, ['VAR1', 'VAR2', 'VAR3'])
            df_plot['anomaly_score'] = output_dataframe['anomaly_score']

            # Plot
            pm.get_plot3D(f'LOF\nn_neighbors={n}-%={percentage_anomalies:.2f}', df_plot, f'./files/output/LOF/images/LOF-n{n}.png')

# Get common outliers
get_common_outliers()
