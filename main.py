from app import create_app
from app.system_db.admin import AdminCRUD

'''
admin login 
username: Aleksey
password: 123
'''

if __name__ == "__main__":
    app = create_app()
    app.run()