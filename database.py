from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRESQL_LINK = "postgresql://postgres:1234@localhost:5432/nexgen"

engine = create_engine(POSTGRESQL_LINK)

SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

base = declarative_base()


