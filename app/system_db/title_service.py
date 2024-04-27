from app.system_db.models import TitleService
from app.system_db import db_session,Base
from sqlalchemy import text
from pydantic import validate_call
from app.system_db.basic import BasicCRUD

class TitleServiceCRUD(BasicCRUD):
    @staticmethod
    def add(**params):
        with db_session() as session:
            session.add(TitleService(
                title_service = params.get("title_service"),
                type_service_id = params.get("type_service_id")
                ))
            db_session.commit()

    @staticmethod
    def update(id,**params):
        with db_session() as session:
            session.query(TitleService).filter_by(id=id).update({"title_service":params.get("title_service"),"type_service_id":params.get("type_service_id")})
            db_session.commit()

    @staticmethod
    def get_fk_id(id):
        with db_session() as session:
            fk_id = session.query(TitleService.type_service_id).filter(TitleService.id==id).scalar()
            return fk_id

    @staticmethod
    def get(id):
        with db_session() as session:
            title_service = session.query(TitleService).filter_by(id=id).scalar()
            return title_service
        
    @staticmethod
    def get_fk_data():
        with db_session() as session:
            fk_data = session.query(TitleService).all()
            return fk_data

    
    @staticmethod
    @validate_call
    def get_preview_data(offset:int,columns:list = TitleService.list_display.copy(),tablename:str="title_service"):
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
    def get_types(tablename:str = 'title_service'):
        table_types = {}
        for k,v in Base.metadata.tables.items():
            if v.name == tablename:
                for column in v.columns.items()[1:]:
                    table_types[column[1].name] = (column[1].type,column[1])
        return table_types
    
    @staticmethod
    def delete(id):
        with db_session() as session:
            session.query(TitleService).filter_by(id=id).delete()
            session.commit()


    @staticmethod
    def get_data_by_fk(fk_id):
        with db_session() as session:
            title_services = session.query(TitleService).filter_by(type_service_id=fk_id).all()
            return title_services
    
