from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
# Validate DATABASE_URL
if DATABASE_URL is None:
    raise ValueError(" DATABASE_URL environment variable is not set.")

# Initialize database engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(bind=engine)
