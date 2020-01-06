from config.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from db.models import *
from sqlalchemy import create_engine

from tqdm import tqdm


engine = create_engine(f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4")
