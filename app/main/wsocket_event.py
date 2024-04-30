from app.main.extensions import socketio
from flask_socketio import emit
from app.system_db.message import MessageCRUD

@socketio.on('send_message')
def send_message(message,chat_id,user_id):
    MessageCRUD.add(message=message,chat_id=chat_id,user_id=user_id)
    emit("sucess",{"data":message,"user_id":user_id},broadcast=True,namespace="/")
    return "adsaa"
    