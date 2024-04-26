from app.admin import admin
from app.admin.forms import LoginAdminForm,CustomUpdateForm,CustomAddForm
from flask import render_template,flash,redirect,url_for,session,request
from app.system_db.admin import AdminCRUD
from config import Config
from pydantic import ValidationError
from app.admin.controller import controller_preview_data,controller_get_types,controller_update,controller_add,controller_delete,generate_select_html


@admin.route("/login/",methods={"GET","POST"})
def login():
    if session.get("admin") is None:
        form = LoginAdminForm()
        if form.validate_on_submit():
            username = form.name.data
            password = form.password.data
            admin = AdminCRUD.get_instance(username=username,password=password)
            if admin:
                session["admin"] = admin.id
                return redirect(url_for("admin.main"))
            flash("Данные не коректны")
            return redirect(url_for("admin.login"))
        return render_template("admin/login.html",form=form)
    return redirect(url_for("admin.main"))

@admin.route("/")
def main():
    if session.get("admin"):
        tables = Config.TABLE_COLUMNS
        return render_template("admin/main.html",tables=tables)
    return redirect(url_for("admin.login"))

@admin.route("/<tablename>/")
def table(tablename):
    if session.get("admin"):
        if request.args.get("no_verif"):
            flash("Можно менять и просматривать только свой админ экземпляр!")
        table = Config.TABLE_COLUMNS.get(tablename)
        if table:
            columns = table[0]
            page = request.args.get("page")
            page = page if page else 0
            try:
                preview_data = controller_preview_data(Config.MODELS_CRUD.get(tablename),page)
                return render_template("admin/table.html",columns=columns,preview_data = preview_data,tablename=tablename)
            except ValidationError:
                return redirect(url_for("admin.main"))
    return redirect(url_for("admin.login"))
        
@admin.route("/<tablename>/<instance_id>/",methods={"GET","POST"})
def get_data(tablename,instance_id):
    if session.get("admin"):
        if tablename == 'admin':
            id = session.get("admin")
            if not int(id) == int(instance_id):
                return redirect(url_for("admin.table",tablename=tablename,no_verif=True))
        else:
            id = instance_id
        table_types:dict = controller_get_types(Config.MODELS_CRUD.get(tablename,None))
        form = CustomUpdateForm.generate_input(table_types,instance_id,tablename)
        if request.method == "POST":
            if request.form.get("submit") and form.validate_on_submit():
                params = {k:v for k,v in request.form.items()}
                print(params)
                controller_update(Config.MODELS_CRUD.get(tablename,None),id,params)
                return redirect(url_for("admin.table",tablename=tablename))
            elif request.form.get("delete"):
                return redirect(url_for("admin.delete",tablename=tablename,instance_id=instance_id))
        return render_template("admin/get_data.html",form=form,tablename=tablename,instance_id=instance_id)
    return redirect(url_for("admin.login"))

@admin.route("/<tablename>/add/",methods={"GET","POST"})
def add(tablename):
    if session.get("admin"):
        table_types:dict = controller_get_types(Config.MODELS_CRUD.get(tablename))
        form = CustomAddForm.generate_input(table_types,tablename)
        if form.validate_on_submit():
            params = {k:v for k,v in request.form.items()}
            print(params)
            controller_add(Config.MODELS_CRUD.get(tablename,None),params)
            return redirect(url_for("admin.table",tablename=tablename))
        return render_template("admin/add.html",tablename=tablename,form=form)
    return redirect(url_for("admin.login"))


@admin.route("/<tablename>/delete/<instance_id>")
def delete(tablename,instance_id):
    if session.get("admin"):
        controller_delete(Config.MODELS_CRUD.get(tablename),instance_id)
        return redirect(url_for("admin.table",tablename=tablename))
    return redirect(url_for("admin.login"))

@admin.route("/<tablename>/get_wrape_form/")
def get_wrape_form(tablename):
    parent_id = request.args.get("data")
    return {"wrape_select":f'{generate_select_html(parent_id,tablename)}'}