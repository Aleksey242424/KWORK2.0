from app.main import main
from flask import session,redirect,url_for,render_template,request,flash
from app.system_db.users import UsersCRUD
from app.main.form import CreateProductForm
from app.main.controller import generate_select_title_service_html,generate_select_service_html
from werkzeug.utils import secure_filename
from config import Config
from app.system_db.product import ProductCRUD
from sqlalchemy.exc import DataError

@main.route("/")
def main_page():
    if session.get("id"):
        current_user = UsersCRUD.get(session.get("id"))
        products = ProductCRUD.get_all_by_service(6)
        return render_template("main/main.html",current_user=current_user,products=products)
    return redirect(url_for("auth.login"))

@main.route("/create_product/",methods={"GET","POST"})
def create_product():
    if session.get("id"):
        current_user = UsersCRUD.get(session.get("id"))
        if not current_user.is_customer:
            form = CreateProductForm()
            if request.method == "POST":
                params = {k:v for k,v in request.form.items()}
                file = form.photo.data
                file.filename = secure_filename(f"{current_user.id}_{params.get('title')}.jpg")
                file.save(f"app/static/{Config.MEDIA_DIR}/{file.filename}")
                params["user"] = current_user.id
                params["photo"] = f"{Config.MEDIA_DIR}/{file.filename}"
                try:
                    ProductCRUD.add(**params,)
                    return redirect(url_for("profile.profile_page"))
                except DataError:
                    flash("Данные не коректны")
                    return redirect(url_for("main.create_product"))
            return render_template("main/create_product.html",form=form)
    return redirect(url_for("auth.login"))



@main.route("/create_product/get_wrape_form/")
def get_wrape_form():
    parent_id = request.args.get("data")
    select = generate_select_title_service_html(parent_id)
    return {"wrape_select":f'{select[0]}',"wrape_select_service":f'{select[1]}'}


@main.route("/create_product/get_wrape_title_service_form/")
def get_wrape_service_form():
    parent_id = request.args.get("data")
    return {"wrape_select_service":f'{generate_select_service_html(parent_id)}'}