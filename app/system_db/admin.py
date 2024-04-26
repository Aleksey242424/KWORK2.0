from app.system_db.models import Admin
from app.system_db import db_session,Base
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import text
from pydantic import validate_call
from app.system_db.basic import BasicCRUD

class AdminCRUD(BasicCRUD):
    @staticmethod
    def add(username,password):
        with db_session() as session:
            session.add(Admin(
                username=username,
                hash_password=generate_password_hash(password=password)
                ))
            db_session.commit()

    @staticmethod
    def update(id,**params):
        with db_session() as session:
            session.query(Admin).filter_by(id=id).update({"username":params.get("username"),"hash_password":generate_password_hash(params.get("hash_password"))})
            db_session.commit()
    @staticmethod
    def get_instance(username,password):
        with db_session() as session:
            try:
                admin = session.query(Admin).filter(Admin.username == username,check_password_hash(
                    session.query(Admin.hash_password).filter_by(username=username).scalar(),
                    password
                ) == True).scalar()
                return admin
            except AttributeError:
                return 

    @staticmethod
    def get(admin_id):
        with db_session() as session:
            admin = session.query(Admin).filter_by(id=admin_id).scalar()
            return admin

    
    @staticmethod
    @validate_call
    def get_preview_data(offset:int,columns:list = Admin.list_display,tablename:str="admin"):
        if "hash_password" in columns:
            columns.remove("hash_password")
        """
        Понимаю все риски насчёт sql инъекций,но другого решения не придумал,
        НО всё под контролем т.к. типы данных валидируются через пайдентик
        """
        if not 'id' in columns:
            columns.insert(0,'id')
        params = ','.join([column for column in columns])
        query = """SELECT %s FROM %s OFFSET %s LIMIT 10;"""%(params,tablename,offset)
        query = text(query)
        with db_session() as session:
            data = session.execute(query)
            return data
        
    @staticmethod
    def get_types(tablename:str = 'admin'):
        table_types = {}
        for k,v in Base.metadata.tables.items():
            if v.name == tablename:
                for column in v.columns.items()[1:]:
                    table_types[column[1].name] = (column[1].type,column[1])
        return table_types
    
    @staticmethod
    def delete(id):
        with db_session() as session:
            session.query(Admin).filter_by(id=id).delete()
            session.commit()
    
    