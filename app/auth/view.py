from app.auth import auth
from flask import render_template,redirect,url_for,request,session,flash
from app.auth.forms import LoginForm,RegisterForm
from app.system_db.users import UsersCRUD

@auth.route("/",methods={"GET","POST"})
def login():
    if session.get("id") is None:
        form = LoginForm()
        if form.validate_on_submit():
            params = {k:v for k,v in request.form.items()}
            user = UsersCRUD.get_instance(username=params["name"],password=params["hash_password"])
            if user:
                session["id"] = user.id
                return redirect(url_for("main.main_page"))
            flash("Данные не коректны")
            return redirect(url_for("auth.login"))
        return render_template("auth/login.html",form=form)
    return redirect(url_for("main.main_page"))

@auth.route("/register/",methods={"GET","POST"})
def register():
    if session.get("id")  is None:
        form = RegisterForm()
        if form.validate_on_submit() and form.phone.data.isdigit():
            params = {k:v for k,v in request.form.items()}
            if UsersCRUD.add(**params,):
                session["id"] = UsersCRUD.get_instance(username=params["name"],password=params["hash_password"]).id
                return redirect(url_for("main.main_page"))
            flash("Пользователь с такими данными уже зарегестрирован")
            return redirect(url_for("auth.register"))
        if form.errors:
            flash("Данные не коректны")
        return render_template("auth/register.html",form=form)
    return redirect(url_for("main.main_page"))