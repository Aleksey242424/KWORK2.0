from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker,scoped_session

from dotenv import load_dotenv
from os import getenv
load_dotenv()

DB_CONN = f'{getenv("DB_DIALECT")}+{getenv("DB_API")}://{getenv("DB_USER")}:{getenv("DB_PASSWORD")}@{getenv("DB_HOST")}:{getenv("DB_PORT")}/{getenv("DB_NAME")}'

engine = create_engine(DB_CONN)

db_session = scoped_session(sessionmaker(bind=engine,autoflush=False,expire_on_commit=False,autocommit=False))

class Base(DeclarativeBase):
    pass

