from app import create_app
from app.system_db.admin import AdminCRUD

'''
admin login 
username: Aleksey
password: megapythondeveloper123
'''

if __name__ == "__main__":
    AdminCRUD.update(id=1,username = "Aleksey",hash_password = "123" )
    app = create_app()
    app.run()