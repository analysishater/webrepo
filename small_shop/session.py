from sqlalchemy.orm import sessionmaker
from model import engine

def get_db():

    SessionLocal = sessionmaker(bind=engine) 
    
    db = SessionLocal()  # Create session (not Sessionmaker)
    try:
        yield db          # Give session to endpoint 
    finally:              # finally
        db.close()        # Close session when done

