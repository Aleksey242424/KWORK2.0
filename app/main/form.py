from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,IntegerField,SelectField,FileField
from wtforms.validators import DataRequired,Length
from app.system_db.type_service import TypeServiceCRUD
from app.system_db.title_service import TitleServiceCRUD
from app.system_db.service import ServiceCRUD


class CreateProductForm(FlaskForm):
    title = StringField(label="title",render_kw={"placeholder":"title"},validators=[DataRequired(),Length(4,20)])
    info = TextAreaField(label="info",render_kw={"placeholder":"description"},validators=[DataRequired(),Length(0,100)])
    price = IntegerField(label="price",render_kw={"placeholder":"price"},validators=[DataRequired()])
    photo = FileField(label="Загрузить фото")
    type_service_id = TypeServiceCRUD.get_first_id()[0]
    title_service_id = TitleServiceCRUD.get_first_id()[0]
    type_service = SelectField(label='type_service',render_kw={"onchange":"getWrapeSelect(this)"},choices=[(data.id,data.type_service) for data in TypeServiceCRUD.get_fk_data()])
    title_service = SelectField(label='title_service',render_kw={"onchange":"getWrapeSelectService(this)"},choices=[(data.id,data.title_service) for data in TitleServiceCRUD.get_data_by_fk(type_service_id)])
    wrape_select_service = SelectField(label='service',choices=[(data.id,data.service) for data in ServiceCRUD.get_fk_data(title_service_id)])


class FilterForm(FlaskForm):
    type_service_id = TypeServiceCRUD.get_first_id()[0]
    title_service_id = TitleServiceCRUD.get_first_id()[0]
    type_service = SelectField(label='type_service',render_kw={"onchange":"getWrapeSelect(this)"},choices=[(data.id,data.type_service) for data in TypeServiceCRUD.get_fk_data()])
    title_service = SelectField(label='title_service',render_kw={"onchange":"getWrapeSelectService(this)"},choices=[(data.id,data.title_service) for data in TitleServiceCRUD.get_data_by_fk(type_service_id)])
    wrape_select_service = SelectField(label='service',choices=[(data.id,data.service) for data in ServiceCRUD.get_fk_data(title_service_id)])
    start_price = IntegerField(label="price",render_kw={"placeholder":"от","oninput":"generateProduct()"})
    end_price = IntegerField(label="price",render_kw={"placeholder":"до","oninput":"generateProduct()"})

class ChatMessageForm(FlaskForm):
    message = StringField(label="message",render_kw={"placeholder":"message"},validators=[DataRequired(),Length(1,1000)])
    