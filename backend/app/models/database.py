from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL
# Using SQLite for development
SQLALCHEMY_DATABASE_URL = "sqlite:///./chatbot.db"

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create baseclass
Base = declarative_base()

# FastAPI route will call this function to create session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()