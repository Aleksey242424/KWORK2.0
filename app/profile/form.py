from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,IntegerField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length
from app.system_db.type_service import TypeServiceCRUD
from app.system_db.title_service import TitleServiceCRUD
from app.system_db.service import ServiceCRUD

class UpdateProfileForm(FlaskForm):
    name = StringField(label="username",render_kw={'placeholder':'username'},validators=[DataRequired(),Length(0,30)])
    email = EmailField(label="email",render_kw={"placeholder":"email"},validators=[DataRequired(),Length(0,50)])
    phone = IntegerField(label="phone",render_kw={"oninput":"validatorPhone()","placeholder":"phone"},validators=[DataRequired()])


def update_product(type_service_id,title_service_id,service_id):
    class UpdateProductForm(FlaskForm):
        pass
    type_service = TypeServiceCRUD.get(type_service_id)
    title_service = TitleServiceCRUD.get(title_service_id)
    service_id = ServiceCRUD.get(service_id)
    inputs = {"title":StringField(label="username",render_kw={'placeholder':'title'},validators=[DataRequired(),Length(0,20)]),
    "info":TextAreaField(label="description",render_kw={"placeholder":"description"},validators=[DataRequired(),Length(0,100)]),
    "price":IntegerField(label="price",render_kw={"placeholder":"price"},validators=[DataRequired()]),
    "type_service":SelectField(label='type_service',render_kw={"onchange":"getWrapeSelect(this)"},choices=[(data.id,data.type_service) for data in TypeServiceCRUD.get_fk_data()],default=type_service.id),
    "title_service":SelectField(label='title_service',render_kw={"onchange":"getWrapeSelectService(this)"},choices=[(data.id,data.title_service) for data in TitleServiceCRUD.get_data_by_fk(type_service.id)],default=title_service.id),
    "wrape_select_service":SelectField(coerce=int,validate_choice=False,label='service',choices=[(data.id,data.service) for data in ServiceCRUD.get_fk_data(title_service.id)],default=service_id.id)}
    for k,v in inputs.items():
        setattr(UpdateProductForm,k,v)
    return UpdateProductForm()
