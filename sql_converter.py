# Import Dependencies
import pandas as pd
import sqlalchemy

# Create Engines
source_engine = sqlalchemy.create_engine('postgresql+psycopg2://user:password@hostname/database_name')
target_engine = sqlalchemy.create_engine('sqlite:///{target_sqlite_name}.db')

# Establish Connections
source_conn = source_engine.connect()
target_conn = target_engine.connect()

# Using pandas to read data out of SQL
my_data_df = pd.read_sql("SELECT * FROM {dn_name}", source_conn)

# Move data to SQLite file
my_data_df.to_sql('{target_sqlite_name}', target_conn, if_exists="replace")