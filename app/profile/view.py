from app.profile import profile
from flask import session,redirect,url_for,render_template
from app.system_db.users import UsersCRUD


@profile.route("/customer/")
def customer_profile():
    if session.get("id"):
        current_user = UsersCRUD.get(session.get("id"))
        if current_user.is_customer:
            return render_template("profile/customer_profile.html",current_user=current_user)
        return redirect(url_for("main.main_page"))
    return redirect(url_for("auth.login"))

@profile.route("/executor/")
def executor_profile():
    if session.get("id"):
        current_user = UsersCRUD.get(session.get("id"))
        if not current_user.is_customer:
            return render_template("profile/executor_profile.html",current_user=current_user)
        return redirect(url_for("main.main_page"))
        
    return redirect(url_for("auth.login"))