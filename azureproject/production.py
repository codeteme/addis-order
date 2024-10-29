import os

# Load environment variables for production database connection
print("Prod test")

# Get the connection string from environment variable
conn_str = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING')
if not conn_str:
    raise ValueError("Error: AZURE_POSTGRESQL_CONNECTIONSTRING environment variable is not set.")

print("conn_str is not empty")

# Parse the connection string into a dictionary of parameters
try:
    conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}
except (IndexError, ValueError) as e:
    raise ValueError("Error parsing connection string. Ensure it is in 'keyword=value' format.") from e

print("Parsed connection parameters:", conn_str_params)

# Check for required parameters and print them for verification
required_keys = ['user', 'password', 'host', 'dbname', 'sslmode']
for key in required_keys:
    if key not in conn_str_params:
        raise KeyError(f"Missing required connection parameter: {key}")
    print(f"{key}: {conn_str_params[key]}")

# Construct the DATABASE_URI for SQLAlchemy
DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}?sslmode={sslmode}'.format(
    dbuser=conn_str_params['user'],
    dbpass=conn_str_params['password'],
    dbhost=conn_str_params['host'],
    dbname=conn_str_params['dbname'],
    sslmode=conn_str_params['sslmode']
)

print("DATABASE_URI constructed successfully:", DATABASE_URI)