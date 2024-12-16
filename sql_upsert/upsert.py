import sqlalchemy
from sqlalchemy import text

def create_table_with_unique_constraint(table_name, engine, unique_columns):
    """
    Create a new table with unique constraints and copy data from old table.
    
    Args:
        table_name (str): Name of the table to create
        engine (sqlalchemy.Engine): SQLAlchemy engine instance
        unique_columns (list): List of column names to make unique
        
    Returns:
        None
    """
    inspector = sqlalchemy.inspect(engine)
    columns = inspector.get_columns(table_name)
    
    cols_sql = ', '.join([f'{col["name"]} {col["type"]}' for col in columns])
    unique_cols = ', '.join(unique_columns)
    
    temp_table = f"{table_name}_temp"
    create_sql = f'CREATE TABLE {temp_table} ({cols_sql}, UNIQUE({unique_cols}) ON CONFLICT REPLACE)'
    
    with engine.begin() as conn:
        conn.execute(text(create_sql))
        conn.execute(text(f"INSERT INTO {temp_table} SELECT * FROM {table_name}"))
        conn.execute(text(f"DROP TABLE {table_name}"))
        conn.execute(text(f"ALTER TABLE {temp_table} RENAME TO {table_name}"))

def to_sql_upsert(df, table_name, engine, unique_columns):
    """
    Write DataFrame to SQL with upsert functionality.
    
    Args:
        df (pandas.DataFrame): DataFrame to write
        table_name (str): Name of target SQL table
        engine (sqlalchemy.Engine): SQLAlchemy engine instance
        unique_columns (list): List of columns for unique constraint
        
    Returns:
        pandas.DataFrame: The DataFrame that was written to SQL
        
    Usage:
        >>> import pandas as pd
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine('sqlite:///example.db')
        >>> df = pd.DataFrame({'id': [1, 2], 'value': ['a', 'b']})
        >>> df_written = to_sql_upsert(df, 'my_table', engine, ['id'])
    """
    inspector = sqlalchemy.inspect(engine)
    
    has_constraint = False
    if inspector.has_table(table_name):
        unique_constraints = inspector.get_unique_constraints(table_name)
        for constraint in unique_constraints:
            if set(constraint['column_names']) == set(unique_columns):
                has_constraint = True
                break
    
    df.to_sql(table_name, engine, if_exists='append', index=False)
    
    if not has_constraint:
        create_table_with_unique_constraint(table_name, engine, unique_columns)
        
    return df
    