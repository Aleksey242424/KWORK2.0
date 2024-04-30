from sqlalchemy.orm import Mapped,mapped_column
from app.system_db import Base
from sqlalchemy.types import String,Integer,VARCHAR
from sqlalchemy import ForeignKey

class Admin(Base):
    __tablename__ = 'admin'
    """
    list_display работает по томуже принципу что и одноимённый атрибут в Django.
    Не сущеситвующие колонки будут проигнорируемы,связаные данные не поддерживает для вывода
    """
    list_display = ["username","hash_password"]

    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(String(50),unique=True)
    hash_password:Mapped[str]

class TypeService(Base):
    __tablename__ = 'type_service'
    list_display = ["type_service"]
    id:Mapped[int] = mapped_column(primary_key=True)
    type_service:Mapped[str] = mapped_column(String(40),unique=True)

class TitleService(Base):
    __tablename__ = "title_service"
    list_display = ["title_service"]
    id:Mapped[int] = mapped_column(primary_key=True)
    title_service:Mapped[str] = mapped_column(String(90),unique=True)
    type_service_id:Mapped[int] = mapped_column(ForeignKey("type_service.id",ondelete="CASCADE",onupdate="CASCADE"))

class Service(Base):
    __tablename__ = "service"
    list_display = ["service"]
    id:Mapped[int] = mapped_column(primary_key=True)
    service:Mapped[str] = mapped_column(String(90),unique=True)
    title_service_id:Mapped[int] = mapped_column(ForeignKey("title_service.id",ondelete="CASCADE",onupdate="CASCADE"))

class Users(Base):
    __tablename__ = 'users'
    list_display = ["name","phone","email","is_customer"]
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(30),unique=True)
    hash_password:Mapped[str] = mapped_column(String(300))
    email:Mapped[str] = mapped_column(String(50),unique=True)
    phone:Mapped[str] = mapped_column(String(11),unique=True)
    is_customer:Mapped[bool] = mapped_column(default=False) 


class Product(Base):
    __tablename__ = "product"
    list_display = ["title","price","user"]
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(String(20))
    info:Mapped[str] = mapped_column(VARCHAR(1000),nullable=True)
    photo:Mapped[str] = mapped_column(String(250))
    price:Mapped[int] = mapped_column(Integer)
    user:Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE",onupdate="CASCADE"))
    service:Mapped[int] = mapped_column(ForeignKey("service.id",ondelete="CASCADE",onupdate="CASCADE"))


class Message(Base):
    __tablename__ = "message"
    list_display = ["message","user_id","chat_id"]
    message:Mapped[str] = mapped_column(String(1000))
    user:Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE",onupdate="CASCADE"),primary_key=True)
    user_:Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE",onupdate="CASCADE"),primary_key=True)