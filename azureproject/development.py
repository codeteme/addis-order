import os

# Dev environment test
print("Dev Test")

# Ensure all required environment variables are present
required_env_vars = ['DBUSER', 'DBPASS', 'DBHOST', 'DBNAME']
for var in required_env_vars:
    if var not in os.environ:
        raise EnvironmentError(f"Error: Missing required environment variable '{var}'.")

# Construct the DATABASE_URI for SQLAlchemy
DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'],
    dbname=os.environ['DBNAME']
)

print("DATABASE_URI constructed successfully:", DATABASE_URI)