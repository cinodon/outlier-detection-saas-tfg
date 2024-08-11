# engine/engine.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Path to the secrets
password_file_path = '/run/secrets/db-password'

with open(password_file_path, 'r') as file:
    db_password = file.read().strip()

# Connection Settings
DATABASE_URL = f"postgresql://postgres:{db_password}@db:5432/company148"

# Create Engine
engine = create_engine(DATABASE_URL)

# Create session
Session = sessionmaker(bind=engine)
session = Session()
