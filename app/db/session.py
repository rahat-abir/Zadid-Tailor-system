from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    future=True,
    echo=False,  # set True if you want SQL logs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
