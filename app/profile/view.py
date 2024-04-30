from app.profile import profile
from flask import session,redirect,url_for,render_template,request,flash
from app.system_db.users import UsersCRUD
from app.system_db.product import ProductCRUD
from app.system_db.type_service import TypeServiceCRUD
from app.profile.form import UpdateProfileForm,update_product
from app.profile.controller import generate_select_title_service_html,generate_select_service_html
from app.redis.cache_history import get_history


@profile.route("/")
def profile_page():
    if session.get("id"):
        current_user = UsersCRUD.get(session.get("id"))
        if current_user.is_customer:
            return redirect(url_for("profile.customer_profile"))
        else:
            return redirect(url_for("profile.executor_profile"))
    return redirect(url_for("auth.login"))

@profile.route("/customer/",methods={"GET","POST"})
def customer_profile():
    if session.get("id"):
        current_user = UsersCRUD.get(session.get("id"))
        if current_user.is_customer:
            form = UpdateProfileForm()
            if form.validate_on_submit():
                params = {k:v for k,v in request.form.items()}
                if not UsersCRUD.update_from_profile(current_user.id,**params,):
                    flash("Пользователь с такими данными уже зарегестрирован")
                return redirect(url_for("profile.customer_profile"))
            history_products = get_history(current_user.id)
            return render_template("profile/customer_profile.html",current_user=current_user,form=form,history_products=history_products)
        return redirect(url_for("main.main_page"))
    return redirect(url_for("auth.login"))

@profile.route("/executor/",methods={"GET","POST"})
def executor_profile():
    if session.get("id"):
        current_user = UsersCRUD.get(session.get("id"))
        if not current_user.is_customer:
            user_products = ProductCRUD.get_product_for_users(current_user.id)
            form = UpdateProfileForm()
            if form.validate_on_submit():
                params = {k:v for k,v in request.form.items()}
                if not UsersCRUD.update_from_profile(current_user.id,**params,):
                    flash("Пользователь с такими данными уже зарегестрирован")
                return redirect(url_for("profile.executor_profile"))
            return render_template("profile/executor_profile.html",current_user=current_user,user_products=user_products,form=form)
        return redirect(url_for("main.main_page"))
        
    return redirect(url_for("auth.login"))


@profile.route("/executor/product/<id>/",methods={"GET","POST"})
def user_product(id):
    if session.get("id"):
        current_user = UsersCRUD.get(session.get("id"))
        current_product = ProductCRUD.get_for_users(id)
        if not current_user.is_customer and current_user.id == current_product[0][0].user:
            service_id = current_product[0][1].id
            title_service_id = current_product[0][2].id
            type_service_id = TypeServiceCRUD.get_id_by_title_service(current_product[0][2].type_service_id)
            form = update_product(service_id=service_id,title_service_id=title_service_id,type_service_id=type_service_id)
            if form.validate_on_submit():
                params = {k:v for k,v in request.form.items()}
                ProductCRUD.update_for_user(current_product[0][0].id,**params,)
                return redirect(url_for("profile.user_product",id=id))
            return render_template("profile/user_product.html",current_product=current_product,current_user=current_user,form=form)
        return redirect(url_for("main.main_page"))
        
    return redirect(url_for("auth.login"))


@profile.route("/executor/product/<id>/get_wrape_form/")
def get_wrape_form(id):
    parent_id = request.args.get("data")
    select = generate_select_title_service_html(parent_id)
    return {"wrape_select":f'{select[0]}',"wrape_select_service":f'{select[1]}'}


@profile.route("/executor/product/<id>/get_wrape_title_service_form/")
def get_wrape_service_form(id):
    parent_id = request.args.get("data")
    return {"wrape_select_service":f'{generate_select_service_html(parent_id)}'}