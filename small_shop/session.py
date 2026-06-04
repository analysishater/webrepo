from sqlalchemy.orm import sessionmaker
from connection import engine  # Import from connection.py

# Create session factory
SessionLocal = sessionmaker(bind=engine)

# Session function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()