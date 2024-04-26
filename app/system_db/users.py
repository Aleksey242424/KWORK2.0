from app.system_db.models import Users
from app.system_db import db_session,Base
from sqlalchemy import text
from pydantic import validate_call
from app.system_db.basic import BasicCRUD
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.exc import IntegrityError

class UsersCRUD(BasicCRUD):
    @staticmethod
    def add(**params):
        with db_session() as session:
            try:
                session.add(Users(
                    name = params.get("name"),
                    hash_password = generate_password_hash(params.get("hash_password")),
                    email = params.get("email"),
                    phone = params.get("phone"),
                    is_customer = True if params.get("is_customer") == "y" else False
                    ))
                db_session.commit()
                return True
            except IntegrityError as ex:
                return 

    @staticmethod
    def update(id,**params):
        with db_session() as session:
            print(params)
            session.query(Users).filter_by(id=id).update({"name":params.get("name"),"email":params.get("email"),"phone":params.get("phone"),"hash_password":generate_password_hash(params.get("hash_password"))})
            db_session.commit()

    @staticmethod
    def get(id):
        with db_session() as session:
            users = session.query(Users).filter_by(id=id).scalar()
            return users
        
    @staticmethod
    def get_instance(username,password):
        with db_session() as session:
            try:
                users = session.query(Users).filter(Users.name==username,
                                                    check_password_hash(
                    session.query(Users.hash_password).filter(Users.name == username).scalar(),
                    password
                ) == True).scalar()
                return users
            except AttributeError:
                return
        
    @staticmethod
    def get_fk_data():
        with db_session() as session:
            fk_data = session.query(Users).all()
            return fk_data

    
    @staticmethod
    @validate_call
    def get_preview_data(offset:int,columns:list = Users.list_display.copy(),tablename:str="users"):
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
    def get_types(tablename:str = 'users'):
        table_types = {}
        for k,v in Base.metadata.tables.items():
            if v.name == tablename:
                for column in v.columns.items()[1:]:
                    table_types[column[1].name] = (column[1].type,column[1])
        return table_types
    
    @staticmethod
    def delete(id):
        with db_session() as session:
            session.query(Users).filter_by(id=id).delete()
            session.commit()

    @staticmethod
    def get_phone(id):
        with db_session() as session:
            user = session.query(Users).filter_by(id=id).scalar()
            print(user.phone)
            return user.phone


    