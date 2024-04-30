from app.system_db.models import Chat,Users
from app.system_db import db_session
from sqlalchemy.exc import IntegrityError


class ChatCRUD():
    @staticmethod
    def add(user_,user_id):
        with db_session() as session:
            try:
                session.add(Chat(user_=user_,user=user_id))
                db_session.commit()
            except IntegrityError as ex:
                print(ex)
        
    @staticmethod
    def get(user_,user):
        with db_session() as session:
            chat = session.query(Chat).filter_by(user_=user_,user=user).scalar()
            return chat
        
    @staticmethod
    def get_by_id(id):
        with db_session() as session:
            chat = session.query(Chat).filter_by(id=id).scalar()
            return chat
        
    @staticmethod
    def get_chat_for_customer(id):
        with db_session() as session:
            chats = session.query(Chat,Users).join(Users,Chat.user_==Users.id).filter(Chat.user==id).all()
            return chats
    
    @staticmethod
    def get_chat_for_executor(id):
        with db_session() as session:
            chats = session.query(Chat,Users).join(Users,Chat.user==Users.id).filter(Chat.user_==id).all()
            return chats
    