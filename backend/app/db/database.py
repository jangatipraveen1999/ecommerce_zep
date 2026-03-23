from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    # PostgreSQL specific settings
    pool_size=10,           # number of connections in pool
    max_overflow=20,        # extra connections beyond pool_size
    pool_pre_ping=True,     # verify connection is alive before using
    pool_recycle=300,       # recycle connections every 5 minutes
    echo=settings.DEBUG,    # log SQL queries in debug mode
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
