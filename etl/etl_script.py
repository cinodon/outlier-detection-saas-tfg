import yaml
from modules import data_processing as dp
from modules import db_processor as db
from modules import clustering_models as cm
from modules import plot_management as pm

def isolation_forest(input_df_scaled, output_dataframe, ne, ms, c):
    # Execute model
    output_dataframe['anomaly_score'] = cm.execute_isolation(input_df_scaled, ne, ms, c)

    # Get percentage of outliers
    num_anomalies = (output_dataframe['anomaly_score'] == -1).sum()
    total_entries = len(output_dataframe)
    percentage_anomalies = (num_anomalies / total_entries) * 100

    # Print percentage
    print(f'For IF with n_estimators {ne}, max_samples {ms}, contamintation {c}: {percentage_anomalies:.2f}%')

    return output_dataframe['anomaly_score']

def if_save_file(output_dataframe):
    output_file = f'./files/output/IF/data/IF-ne{ne}-ms{ms}-c{c}.csv'
    dp.save_to_csv(output_dataframe, output_file)

def if_save_plot_file(output_dataframe, input_df_scaled):
    input_df_pca = dp.tsne_reduce_dimensions(input_df_scaled)

    # Convertir a DataFrame y añadir la columna 'anomaly_score'
    df_pca = dp.transform_to_dataframe(input_df_pca, ['PC1', 'PC2'])

    # Transform found clusters into 1 (inliers)
    output_dataframe['anomaly_score'] = dp.clusters_to_inliers(output_dataframe['anomaly_score'])
    df_pca['anomaly_score'] = output_dataframe['anomaly_score']

    # Plot
    pm.get_plot(f'Isolation Forest\nn_estimators={ne}-max_samples={ms}-cont.{c}', df_pca,
                f'./files/output/IF/images/IF-ne{ne}-ms{ms}-cont{c}.png')

def dbscan(input_df_scaled, output_dataframe, e, ms):
    # Execute model
    output_dataframe['anomaly_score'] = cm.execute_dbscan(input_df_scaled, e, ms)

    # Get percentage of outliers
    num_anomalies = (output_dataframe['anomaly_score'] == -1).sum()
    total_entries = len(output_dataframe)
    percentage_anomalies = (num_anomalies / total_entries) * 100

    # Print percentage
    print(f'For DBSCAN with eps {e}, min_samples {ms}: {percentage_anomalies:.2f}%')

    return output_dataframe['anomaly_score']

def dbscan_save_file(output_dataframe):
    output_file = f'./files/output/DBSCAN/data/DBSCAN-eps{e}-ms{ms}.csv'
    dp.save_to_csv(output_dataframe, output_file)

def dbscan_save_plot_file(output_dataframe, input_df_scaled):
    input_df_pca = dp.tsne_reduce_dimensions(input_df_scaled)

    # Convertir a DataFrame y añadir la columna 'anomaly_score'
    df_pca = dp.transform_to_dataframe(input_df_pca, ['PC1', 'PC2'])
    # Transform found clusters into 1 (inliers)
    output_dataframe['anomaly_score'] = dp.clusters_to_inliers(output_dataframe['anomaly_score'])
    df_pca['anomaly_score'] = output_dataframe['anomaly_score']

    # Plot
    pm.get_plot(f'DBSCAN\neps={e}-min_samples={ms}', df_pca,
                f'./files/output/DBSCAN/images/DBSCAN-eps{e}-ms{ms}.png')

def lof(input_df_scaled, output_dataframe, n):
    # Execute model
    output_dataframe['anomaly_score'] = cm.execute_lof(input_df_scaled, n)

    # Get percentage of outliers
    num_anomalies = (output_dataframe['anomaly_score'] == -1).sum()
    total_entries = len(output_dataframe)
    percentage_anomalies = (num_anomalies / total_entries) * 100

    # Print percentage
    print(f'For LOF with n_neighbors {n}: {percentage_anomalies:.2f}%')

def lof_save_file(output_dataframe):
    output_file = f'./files/output/LOF/data/LOF-n{n}.csv'
    dp.save_to_csv(output_dataframe, output_file)

def lof_save_plot_file(output_dataframe, input_df_scaled):
    input_df_pca = dp.tsne_reduce_dimensions(input_df_scaled)

    # Transform to dataframe and add column 'anomaly_score'
    df_pca = dp.transform_to_dataframe(input_df_pca, ['PC1', 'PC2'])
    df_pca['anomaly_score'] = output_dataframe['anomaly_score']

    # Plot
    pm.get_plot(f'TLOF\nn_neighbors={n}', df_pca,
                f'./files/output/LOF/images/LOF-n{n}.png')

if __name__ == '__main__':
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

    # Get base output file
    if not connect_database:
        output_dataframe = dp.load_csv('./files/output/output-base.csv')

    # Select Model 0 - Isolation Forest | 1 - LoF | 2 - DBSCAN
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
                    output_dataframe['anomaly_score'] = isolation_forest(input_df_scaled, output_dataframe, ne, ms, c)

                    # Save data
                    if if_save_data:
                        if_save_file(output_dataframe)

                    # Save plot
                    if if_save_plot:
                        if_save_plot_file(output_dataframe, input_df_scaled)

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
                output_dataframe['anomaly_score'] = dbscan(input_df_scaled, output_dataframe, e, ms)

                # Save data
                if dbscan_save_data:
                    dbscan_save_file(output_dataframe)

                # Save plot
                if dbscan_save_plot:
                    dbscan_save_plot_file(output_dataframe, input_df_scaled)

    # Local Outlier Factor
    run_lof = config['run_lof']
    n_neighbors = config['n_neighbors']
    lof_save_data = config['lof_save_data']
    lof_save_plot = config['lof_save_plot']
    if run_lof:
        for n in n_neighbors:
            output_dataframe['anomaly_score'] = lof(input_df_scaled, output_dataframe, n)

            # Save data
            if lof_save_data:
                lof_save_file(output_dataframe)

            # Save plot
            if lof_save_plot:
                lof_save_plot_file(output_dataframe, input_df_scaled)


