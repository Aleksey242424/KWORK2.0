from app.main import main
from flask import session,redirect,url_for,render_template
from app.system_db.users import UsersCRUD

@main.route("/")
def main_page():
    if session.get("id"):
        current_user = UsersCRUD.get(session.get("id"))
        return render_template("main/main.html",current_user=current_user)
    return redirect(url_for("auth.login"))

@main.route("/create_product")
def create_product():
    if session.get("id"):
        current_user = UsersCRUD.get(session.get("id"))
        if not current_user.is_customer:
            return "create_product"
    return redirect(url_for("auth.login"))