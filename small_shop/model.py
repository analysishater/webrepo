from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from connection import engine

# Create base
Base = declarative_base()
class User(Base):
    __tablename__ = "user"
    
    id_client = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    age = Column(Integer, nullable=False)
    mot_de_pass = Column(String(45), nullable=False)

class Product(Base):
    __tablename__ = "product"
    
    id_product = Column(Integer, primary_key=True, autoincrement=True,unique=True)
    name = Column(String(45), nullable=False,unique=True) 
    quentity = Column(Integer, nullable=False)



# Create tables (if they don't exist)
#Base.metadata.create_all(bind=engine)