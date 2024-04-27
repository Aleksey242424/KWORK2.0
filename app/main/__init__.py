from flask import Blueprint

main = Blueprint(name="main",import_name=__name__,template_folder="templates")


from app.main import view 
