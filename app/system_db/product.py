from app.system_db.models import Product,Service,TitleService
from app.system_db import db_session,Base
from sqlalchemy import text
from pydantic import validate_call
from app.system_db.basic import BasicCRUD
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
from app.redis.cache_product import add_product,update_product

class ProductCRUD(BasicCRUD):
    @staticmethod
    def add(**params):
        with db_session() as session:
            try:
                session.add(Product(
                    title = params.get("title"),
                    info = params.get("info"),
                    price = params.get("price"),
                    photo = params.get("photo"),
                    user = params.get("user"),
                    service = params.get("wrape_select_service")
                    ))
                db_session.commit()
                last_id = ProductCRUD.get_last_id()
                product_data = ProductCRUD.get_for_users(last_id[0])
                add_product(product_id=product_data[0][0].id,product_title=product_data[0][0].title,product_price=product_data[0][0].price,product_photo=product_data[0][0].photo,service = product_data[0][1].service,title_service = product_data[0][2].title_service)
                return True
            except IntegrityError as ex:
                print(ex)
                return 

    @staticmethod
    def update(id,**params):
        with db_session() as session:
            session.query(Product).filter_by(id=id).update({"title":params.get("title"),"price":params.get("price"),"photo":params.get("photo"),"user":params.get("user")})
            db_session.commit()
            
            

    @staticmethod
    def update_for_user(id,**params):
        with db_session() as session:
            session.query(Product).filter_by(id=id).update({"title":params.get("title"),"price":params.get("price"),"info":params.get("info"),"service":params.get("wrape_select_service")})
            db_session.commit()
            product_data = ProductCRUD.get_for_users(id)
            update_product(product_id=product_data[0][0].id,product_title=product_data[0][0].title,product_price=product_data[0][0].price,service = product_data[0][1].service,title_service = product_data[0][2].title_service)

    @staticmethod
    def get(id):
        with db_session() as session:
            product = session.query(Product).filter_by(id=id).scalar()
            return product
        
    @staticmethod
    def get_last_instance():
        with db_session() as session:
            product = session.query(Product).order_by(Product.id.desc()).first()
            return product
        
    @staticmethod
    def get_last_id():
        with db_session() as session:
            last_id = session.query(Product.id).order_by(Product.id.desc()).first()
            return last_id

    @staticmethod
    def get_for_users(id):
        with db_session() as session:
            product = session.query(Product,Service,TitleService).join(
                Service,Product.service==Service.id).join(
                    TitleService,Service.title_service_id == TitleService.id).filter(
                    Product.id==id).all()
            return product
        
    
        
    @staticmethod
    def get_all_by_service(service_id):
        with db_session() as session:
            products = session.query(Product).filter_by(service=service_id).limit(20).all()
            return products
        
    @staticmethod
    def get_instance(username,password):
        with db_session() as session:
            try:
                users = session.query(Product).filter(Product.name==username,
                                                    check_password_hash(
                    session.query(Product.hash_password).filter(Product.name == username).scalar(),
                    password
                ) == True).scalar()
                return users
            except AttributeError:
                return
        
    @staticmethod
    def get_fk_data():
        with db_session() as session:
            fk_data = session.query(Product).all()
            return fk_data
        
    @staticmethod
    def get_product_for_users(user_id):
        with db_session() as session:
            user_products = session.query(Product,Service.service).join(
                Service,Product.service == Service.id).filter(
                    Product.user==user_id).order_by(
                        Product.id.desc()).limit(10).all()
            return user_products

    
    @staticmethod
    @validate_call
    def get_preview_data(offset:int,columns:list = Product.list_display.copy(),tablename:str="prduct"):
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
    def get_types(tablename:str = 'prduct'):
        table_types = {}
        for k,v in Base.metadata.tables.items():
            if v.name == tablename:
                for column in v.columns.items()[1:]:
                    table_types[column[1].name] = (column[1].type,column[1])
        return table_types
    
    @staticmethod
    def delete(id):
        with db_session() as session:
            session.query(Product).filter_by(id=id).delete()
            session.commit()

    @staticmethod
    def get_phone(id):
        with db_session() as session:
            user = session.query(Product).filter_by(id=id).scalar()
            return user.phone

    @staticmethod
    def get_product_by_price_and_service(service_id,start_price="",end_price=""):
        with db_session() as session:
            if end_price and start_price:
                product = session.query(Product).filter(Product.price>=start_price,Product.price<=end_price,Product.service==service_id).all()
            elif end_price:
                product = session.query(Product).filter(Product.price<=end_price,Product.service==service_id).all()
            elif start_price:
                product = session.query(Product).filter(Product.price>=start_price,Product.service==service_id).all()
            else:
                product = session.query(Product).filter(Product.service==service_id).all()
            return product

    