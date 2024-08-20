import uuid
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import SpectralEmbedding, TSNE
from sklearn.preprocessing import MultiLabelBinarizer



def transform_query_data(query_results, cursor):
    column_names = get_column_names(cursor)
    sql_dataframe = create_dataframe(query_results, column_names)

    sql_dataframe = transform_uuid_columns(sql_dataframe, ['workappid', 'userid', 'usermanagerid', 'permissionlevelid'])
    sql_dataframe = fill_na_columns(sql_dataframe, ['workappcategoryid', 'usertypeofworkid', 'userroleid', 'permissionlevelisprivileged'])
    sql_dataframe = transform_is_privileged_column(sql_dataframe, 'permissionlevelisprivileged')

    # Transform Group
    sql_dataframe = transform_usergroupsid_column(sql_dataframe)

    print("Data transformed successfully!")
    return sql_dataframe

def transform_query_to_dataframe(query_results, cursor):
    column_names = get_column_names(cursor)
    sql_dataframe = create_dataframe(query_results, column_names)

    return sql_dataframe


def get_column_names(cursor):
    return [desc[0] for desc in cursor.description]


def create_dataframe(query_results, column_names):
    return pd.DataFrame(query_results, columns=column_names)


def transform_uuid_columns(dataframe, uuid_columns):
    for col in uuid_columns:
        dataframe[col] = dataframe[col].apply(uuid_to_int)
    return dataframe


def uuid_to_int(u):
    return int(uuid.UUID(u).int) if pd.notna(u) else -1


def fill_na_columns(dataframe, columns, fill_value=-1):
    for column in columns:
        dataframe[column] = dataframe[column].fillna(fill_value)
    return dataframe


def transform_is_privileged_column(dataframe, column_name):
    """
    Transform the 'is privileged' column to integers: True -> 1, False -> 0, otherwise -1.
    """
    dataframe[column_name] = dataframe[column_name].apply(lambda x: int(x) if x in [True, False] else -1)
    return dataframe


def transform_usergroupsid_column(sql_dataframe, column_name='usersgroupids'):
    # Función auxiliar para convertir la cadena a una lista de UUIDs
    def parse_groups(group_string):
        if pd.isna(group_string) or group_string == 'NULL':
            return []
        # Limpiar el formato de la cadena y convertirla en una lista de UUIDs
        group_string = group_string.strip('{}').replace("'", "").replace('"', "")
        if group_string:
            return group_string.split(',')
        return []

    # Convertir las cadenas a listas de UUIDs
    sql_dataframe[column_name] = sql_dataframe[column_name].apply(parse_groups)

    # Aplicar MultiLabelBinarizer para convertir los grupos en columnas binarias
    mlb = MultiLabelBinarizer()
    usergroups_encoded = mlb.fit_transform(sql_dataframe[column_name])

    # Convertir los resultados a un DataFrame y concatenarlo con el original
    usergroups_encoded_df = pd.DataFrame(usergroups_encoded, columns=mlb.classes_)
    sql_dataframe = pd.concat([sql_dataframe, usergroups_encoded_df], axis=1)

    # Eliminar la columna original
    sql_dataframe.drop(columns=[column_name], inplace=True)

    return sql_dataframe

def save_to_csv(sql_dataframe, output_path):
    sql_dataframe.to_csv(output_path, header=True, index=False)
    print("Data Transformed and Saved successfully!")

def load_csv(input_path):
    print("Data Read Successfully!")
    return pd.read_csv(input_path)


def exclude_columns(df, excluded_columns):
    columns_to_drop = []

    single_columns = excluded_columns.get('single_columns', [])
    if single_columns:
        columns_to_drop.extend(single_columns)

    column_ranges = excluded_columns.get('column_ranges', [])
    if column_ranges:
        for col_range in column_ranges:
            # Validar que el rango tenga exactamente dos elementos (inicio y fin)
            if len(col_range) == 2:
                start, end = col_range
                if isinstance(start, int) and isinstance(end, int):
                    columns_to_drop.extend(list(range(start, end + 1)))
            else:
                print(f"Advertencia: Rango mal definido {col_range}")

    if columns_to_drop:
        # Asegúrate de que los índices de columna sean válidos para el dataframe
        columns_to_drop = [col for col in columns_to_drop if col < df.shape[1]]

        # Obtener los nombres de las columnas basados en los índices
        columns_to_drop_names = [df.columns[i] for i in columns_to_drop]

        # Eliminar las columnas excluidas del dataframe
        df.drop(columns=columns_to_drop_names, axis=1, inplace=True)

    return df

def transform_to_dataframe(data, columns_name=None):
    return pd.DataFrame(data, columns=columns_name)

def clusters_to_inliers(column):
    return column.apply(lambda x: 1 if x != -1 else -1)

def get_mismatches(df0, df1):
    return df0[df0['anomaly_score'] != df1['anomaly_score']]

def pca_reduce_to_2D(dataframe):
    pca = PCA(n_components=2)
    reduced_dataframe = pca.fit_transform(dataframe)
    return reduced_dataframe


def spectral_embedding_reduce_to_2D(dataframe):
    embedding = SpectralEmbedding(n_components=2)
    data_spectral_2d = embedding.fit_transform(dataframe)
    return data_spectral_2d

def tsne_reduce_to_2D(dataframe):
    tsne = TSNE(n_components=2, perplexity=30, max_iter=1000, random_state=42)
    data_tsne_2d = tsne.fit_transform(dataframe)
    return data_tsne_2d

def spectral_embedding_reduce_to_3D(dataframe):
    embedding = SpectralEmbedding(n_components=3, n_neighbors=15)
    data_spectral_3d = embedding.fit_transform(dataframe)
    return data_spectral_3d

def tsne_reduce_to_3D(dataframe):
    tsne_3d = TSNE(n_components=3, perplexity=30, max_iter=1000, random_state=42)
    data_tsne_3d = tsne_3d.fit_transform(dataframe)
    return data_tsne_3d

def get_common_outliers(df0, df1):
    # Filter dataframes with only the outliers
    df1_filtered = df0[df0['anomaly_score'] == -1]
    df2_filtered = df1[df1['anomaly_score'] == -1]

    # Merge common rows
    common_anomalies = pd.merge(df1_filtered, df2_filtered, how='inner')

    return common_anomalies