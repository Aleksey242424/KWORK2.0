from app.main import main
from flask import session,redirect,url_for,render_template,request,flash
from app.system_db.users import UsersCRUD
from app.main.form import CreateProductForm,FilterForm,ChatMessageForm
from app.main.controller import generate_select_title_service_html,generate_select_service_html,generate_product_by_price_and_service_html
from werkzeug.utils import secure_filename
from config import Config
from app.system_db.product import ProductCRUD
from app.system_db.type_service import TypeServiceCRUD
from app.system_db.title_service import TitleServiceCRUD
from app.system_db.service import ServiceCRUD
from app.system_db.message import MessageCRUD
from sqlalchemy.exc import DataError
from app.redis.cache_history import add_product_in_history


@main.route("/")
def main_page():
    if session.get("id"):
        current_user = UsersCRUD.get(session.get("id"))
        first_type_service_id = TypeServiceCRUD.get_first_id()[0]
        first_title_service_id = TitleServiceCRUD.get_data_by_fk(first_type_service_id)[0].id
        service_id = ServiceCRUD.get_fk_data(first_title_service_id)[0].id
        products = ProductCRUD.get_all_by_service(service_id)
        form=FilterForm()
        return render_template("main/main.html",current_user=current_user,products=products,form=form)
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
            return render_template("main/create_product.html",form=form,current_user=current_user)
    return redirect(url_for("auth.login"))

@main.route("/product/<id>/",methods={"GET","POST"})
def product(id):
    if session.get("id"):
        current_user = UsersCRUD.get(session.get("id"))
        current_product = ProductCRUD.get_for_users(id)
        if current_user.is_customer:
            add_product_in_history(current_product[0][0].id,current_user.id)
        return render_template("main/product.html",current_product=current_product,current_user=current_user)
    return redirect(url_for("auth.login"))

@main.route("/message/")
def message():
    user_  = request.args.get("user_")
    user = UsersCRUD.get(session.get("id"))
    form = ChatMessageForm()
    if form.validate_on_submit():
        message = form.message.data
        MessageCRUD.add(user_=user_,user=user,message=message)
        return redirect(url_for("main.message",user_=user_))
    return render_template("main/message.html")



@main.route("/create_product/get_wrape_form/")
def get_wrape_form():
    parent_id = request.args.get("data")
    select = generate_select_title_service_html(parent_id)
    return {"wrape_select":f'{select[0]}',"wrape_select_service":f'{select[1]}'}


@main.route("/create_product/get_wrape_title_service_form/")
def get_wrape_service_form():
    parent_id = request.args.get("data")
    select = generate_select_service_html(parent_id)
    return {"wrape_select_service":f'{select[0]}'}












@main.route("/get_wrape_form/")
def main_get_wrape_form():
    parent_id = request.args.get("data")
    select = generate_select_title_service_html(parent_id)
    session["service"] = select[2]
    service_id = session.get("service")
    products_html = generate_product_by_price_and_service_html(service_id)
    return {"wrape_select":f'{select[0]}',"wrape_select_service":f'{select[1]}',"products_html":products_html[0],"data":products_html[1]}

@main.route("/get_wrape_title_service_form/")
def main_get_wrape_service_form():
    parent_id = request.args.get("data")
    select = generate_select_service_html(parent_id)
    session["service"] = select[1]
    service_id = session.get("service")
    products_html = generate_product_by_price_and_service_html(service_id)
    return {"wrape_select_service":f'{select[0]}',"products_html":products_html[0],"data":products_html[1]}


@main.route("/get_product_by_price_and_service/")
def get_product_by_price():
    start_price = request.args.get("start_price")
    end_price = request.args.get("end_price")
    service_id = session.get("service")
    first_type_service_id = TypeServiceCRUD.get_first_id()[0]
    first_title_service_id = TitleServiceCRUD.get_data_by_fk(first_type_service_id)[0].id
    service = ServiceCRUD.get_fk_data(first_title_service_id)[0].id
    products_html = generate_product_by_price_and_service_html(service_id,start_price,end_price) if session.get("service") else generate_product_by_price_and_service_html(service,start_price,end_price)        
    return {"products_html":products_html,"products_html":products_html[0],"data":products_html[1]}