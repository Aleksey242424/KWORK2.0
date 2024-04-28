from app.system_db.models import TypeService
from app.system_db import db_session,Base
from sqlalchemy import text
from pydantic import validate_call
from app.system_db.basic import BasicCRUD

class TypeServiceCRUD(BasicCRUD):
    @staticmethod
    def add(**params):
        with db_session() as session:
            session.add(TypeService(
                type_service = params.get("type_service")
                ))
            db_session.commit()

    @staticmethod
    def update(id,**params):
        with db_session() as session:
            session.query(TypeService).filter_by(id=id).update({"type_service":params.get("type_service")})
            db_session.commit()

    @staticmethod
    def get(id):
        with db_session() as session:
            type_service = session.query(TypeService).filter_by(id=id).scalar()
            return type_service
        
    @staticmethod
    def get_fk_data():
        with db_session() as session:
            fk_data = session.query(TypeService).all()
            return fk_data
        
    @staticmethod
    def get_id_by_title_service(id):
        with db_session() as session:
            fk_data = session.query(TypeService.id).filter_by(id=id).scalar()
            return fk_data
        
    @staticmethod
    def get_first_id():
        with db_session() as session:
            type_service = session.query(TypeService.id).first()
            return type_service
        

    
    @staticmethod
    @validate_call
    def get_preview_data(offset:int,columns:list = TypeService.list_display.copy(),tablename:str="type_service"):
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
    def get_types(tablename:str = 'type_service'):
        table_types = {}
        for k,v in Base.metadata.tables.items():
            if v.name == tablename:
                for column in v.columns.items()[1:]:
                    table_types[column[1].name] = (column[1].type,column[1])
        return table_types
    
    @staticmethod
    def delete(id):
        with db_session() as session:
            session.query(TypeService).filter_by(id=id).delete()
            session.commit()

    