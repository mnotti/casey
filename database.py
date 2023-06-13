from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from sqlalchemy import text

# Load the database configuration from JSON
with open('config.json') as f:
    config = json.load(f)

# Extract configuration values
DB_HOST = config['db_host']
DB_PORT = config['db_port']
DB_NAME = config['db_name']
DB_USER = config['db_user']
DB_PASSWORD = config['db_password']

# Create the database connection URL
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create the SQLAlchemy engine
engine = create_engine(DB_URL)

# Create a Session factory
Session = sessionmaker(bind=engine)

# Create a function to get a new database session
def get_session():
    return Session()

# Test the database connection
def test_connection():
    try:
        # Create a new session
        session = get_session()
        
        # Perform a simple query to test the connection
        result = session.execute(text("SELECT 1"))
        print("Database connection successful.")
        print("Result:", result.fetchone())
        
        # Close the session
        session.close()
    except Exception as e:
        print("Database connection error:", str(e))

# Run the test
test_connection()
