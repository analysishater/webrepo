from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection URL
DATABASE_URL = f"mysql+pymysql://{os.getenv('root')}:{os.getenv('khoho')}@{os.getenv('localhost')}:{os.getenv('3603T')}/{os.getenv('small_shop')}"

# Create engine (this is the connection)
engine = create_engine(DATABASE_URL)