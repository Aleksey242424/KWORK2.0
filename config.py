from app.system_db.models import Admin,TypeService,TitleService,Service,Users
from app.system_db.admin import AdminCRUD
from app.system_db.type_service import TypeServiceCRUD
from app.system_db.title_service import TitleServiceCRUD
from app.system_db.service import ServiceCRUD
from app.system_db.users import UsersCRUD
from os import urandom
from os import path
class Config:

    TABLE_COLUMNS = {
        "admin":[[k_ for k_,v_ in v.columns.items() if k_ in  Admin.list_display and k_ != "hash_password"] for k,v in Admin.metadata.tables.items()],
        "type_service":[[k_ for k_,v_ in v.columns.items()] for k,v in TypeService.metadata.tables.items() if v.name == "type_service"],
        "title_service":[[k_ for k_,v_ in v.columns.items()] for k,v in TitleService.metadata.tables.items() if v.name == "title_service"],
        "service":[[k_ for k_,v_ in v.columns.items()] for k,v in Service.metadata.tables.items() if v.name == "service"],
        "users":[[k_ for k_,v_ in v.columns.items()] for k,v in Service.metadata.tables.items() if v.name == "users"]
        }
    
    MODELS_CRUD = {
        "admin":AdminCRUD,
        "type_service":TypeServiceCRUD,
        "title_service":TitleServiceCRUD,
        "service":ServiceCRUD,
        "users":UsersCRUD
    }
        
    SECRET_KEY = urandom(20)
    DEBUG = True
    MEDIA_DIR = "media/product"