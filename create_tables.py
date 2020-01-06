from config.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from db.models import Base
from sqlalchemy import create_engine


if __name__ == "__main__":
    engine = create_engine(f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4")
    Base.metadata.create_all(engine)
