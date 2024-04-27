from flask import Blueprint

admin = Blueprint(name="admin",import_name=__name__,template_folder="templates")


from app.admin import view 
