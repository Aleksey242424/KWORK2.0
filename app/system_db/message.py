from app.system_db.models import Message,Chat,Users
from app.system_db import db_session,Base
from sqlalchemy import text
from pydantic import validate_call
from app.system_db.basic import BasicCRUD
from app.system_db.chat import ChatCRUD

class MessageCRUD(BasicCRUD):
    @staticmethod
    def add(**params):
        with db_session() as session:
            session.add(Message(
                message = params.get("message"),
                chat_id=params.get("chat_id"),
                user=params.get("user_id")
                ))
            
            db_session.commit()

    @staticmethod
    def get_fk_id(id):
        with db_session() as session:
            fk_id = session.query(Message.type_service_id).filter(Message.id==id).scalar()
            return fk_id
        
    @staticmethod
    def get_last():
        with db_session() as session:
            fk_id = session.query(Message).order_by(Message).scalar()
            return fk_id

    @staticmethod
    def get(id):
        with db_session() as session:
            message = session.query(Message).filter_by(id=id).scalar()
            return message
        
    @staticmethod
    def get_all(chat_id):
        with db_session() as session:
            messages = session.query(Message).filter(Message.chat_id==chat_id).all()
            return messages
        
    @staticmethod
    def get_all_messages(user_,user_id):
        with db_session() as session:
            messages = session.query(Message).filter_by(user_=user_,user=user_id).all()
            return messages
        
    @staticmethod
    def get_fk_data():
        with db_session() as session:
            fk_data = session.query(Message).all()
            return fk_data

    
    @staticmethod
    @validate_call
    def get_preview_data(offset:int,columns:list = Message.list_display.copy(),tablename:str="message"):
        """
        Понимаю все риски насчёт sql инъекций,но другого решения не придумал,
        НО всё под контролем т.к. типы данных валидируются через пайдентик
        """
        if not 'id' in columns:
            columns.insert(0,'id')
        params = ','.join([column for column in columns])
        query = """SELECT %s FROM %s OFFSET %s LIMIT 100;"""%(params,tablename,offset)
        query = text(query)
        with db_session() as session:
            data = session.execute(query)
            return data
        
    @staticmethod
    def get_types(tablename:str = 'message'):
        table_types = {}
        for k,v in Base.metadata.tables.items():
            if v.name == tablename:
                for column in v.columns.items()[1:]:
                    table_types[column[1].name] = (column[1].type,column[1])
        return table_types
    
    @staticmethod
    def delete(id):
        with db_session() as session:
            session.query(Message).filter_by(id=id).delete()
            session.commit()


    @staticmethod
    def get_data_by_fk(fk_id):
        with db_session() as session:
            title_services = session.query(Message).filter_by(type_service_id=fk_id).all()
            return title_services
    
    @staticmethod
    def get_first_id():
        with db_session() as session:
            title_service = session.query(Message.id).first()
            return title_service
    
    