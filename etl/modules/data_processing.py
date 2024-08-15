import uuid
import pandas as pd


def transform_data(query_results, cursor):
    column_names = get_column_names(cursor)
    sql_dataframe = create_dataframe(query_results, column_names)

    sql_dataframe = transform_uuid_columns(sql_dataframe, ['workappid', 'userid', 'usermanagerid', 'permissionlevelid'])
    sql_dataframe = fill_na_columns(sql_dataframe, ['workappcategoryid', 'usertypeofworkid', 'userroleid', 'permissionlevelisprivileged'])
    sql_dataframe = transform_is_privileged_column(sql_dataframe, 'permissionlevelisprivileged')

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

def save_to_csv(sql_dataframe, output_path):
    sql_dataframe.to_csv(output_path, header=True, index=False)
    print("Data Transformed and Saved successfully!")