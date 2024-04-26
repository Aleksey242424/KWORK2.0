from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker,scoped_session

engine = create_engine("postgresql+psycopg2://postgres:123@localhost:5432/kwork_2_0")

db_session = scoped_session(sessionmaker(bind=engine,autoflush=False,expire_on_commit=False,autocommit=False))

class Base(DeclarativeBase):
    pass

