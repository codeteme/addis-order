import os

print("Prod test")
# Configure Postgres database based on connection string of the libpq Keyword/Value form
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']

print("conn_str is not empty")

conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}

print("conn_str_params: ", conn_str_params)

print(conn_str_params['user'])
print(conn_str_params['password'])
print(conn_str_params['host'])
print(conn_str_params['dbname'])
print(conn_str_params['sslmode'])

DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}?sslmode={sslmode}'.format(
    dbuser=conn_str_params['user'],
    dbpass=conn_str_params['password'],
    dbhost=conn_str_params['host'],
    dbname=conn_str_params['dbname'],
    sslmode=conn_str_params['sslmode']
)