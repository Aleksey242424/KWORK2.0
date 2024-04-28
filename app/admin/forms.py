from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,IntegerField
from wtforms.validators import DataRequired,Length
from sqlalchemy.types import String,Integer
from app.admin.controller import controller_get_attr,controller_get_fk_data,controller_get_fk_preview,parse_data_fk,get_foreign_tables,get_wrpe_options,get_foreign_tablename,controller_get_crud_model,controller_get_other_data
from config import Config
from app.system_db.service import ServiceCRUD

class LoginAdminForm(FlaskForm):
    name = StringField(label="name",render_kw={"placeholder":"username"},validators=[DataRequired(),Length(0,50)])
    password = PasswordField(label="password",render_kw={"placeholder":"password"},validators=[DataRequired()])

class CustomUpdateForm:
    def generate_input(table_types:dict,instance_id,tablename):
        class UpdateDataForm(FlaskForm):
            pass
        inputs = {}
        UpdateDataForm.values = {}
        for k,v in table_types.items():
            
            if type(v[0]) == type(String()):
                validators = []
                if not v[1].nullable:
                    validators.append(DataRequired())
                if getattr(v[0],"length",None):
                    validators.append(Length(0,v[0].length))
                    input_obj = StringField(label=k,validators=validators)
                else:   
                    input_obj = StringField(label=k,validators=validators)
                
                inputs[k] = input_obj
                UpdateDataForm.values[k] = controller_get_attr(Config.MODELS_CRUD.get(tablename),instance_id,k)
            elif type(v[0]) == type(Integer()):
                fk = v[1].foreign_keys.copy()
                fk_list = list(dict.fromkeys(get_foreign_tables(fk))).copy()[::-1]
                if len(fk_list) > 1:
                    fk = v[1].foreign_keys.copy()
                    fk_table= f"{fk.pop().column.table}"
                    fk_data = controller_get_fk_data(Config.MODELS_CRUD.get(fk_list[0],None))
                    slice_copy = [table for table in fk_list if table != 'type_service']
                    slice_copy.insert(0,tablename)
                    preview_data = controller_get_fk_preview(crud_models=[crud_model for crud_model in controller_get_crud_model(slice_copy)],last_crud_model=Config.MODELS_CRUD.get(f'type_service'),id=instance_id,tablenames=fk_list,tablename = tablename)
                    input_obj = SelectField(id=get_foreign_tablename(fk_table),label=fk_table,render_kw={"onchange":"getWrapeSelect(this)"},validators=validators,choices=[(data[0],f'{data[1]}') for data in parse_data_fk(tablename,fk_data)],default=preview_data.id)
                    del fk_list
                elif len(fk_list) == 1:
                    fk = v[1].foreign_keys.copy()
                    fk_table= f"{fk.pop().column.table}"
                    fk_data = controller_get_fk_data(Config.MODELS_CRUD.get(fk_table,None))
                    preview_data = controller_get_fk_preview(crud_models=[crud_model for crud_model in controller_get_crud_model([tablename])],last_crud_model=Config.MODELS_CRUD.get("type_service"),id=instance_id,tablenames=fk_list,tablename = tablename)
                    input_obj = SelectField(label=k,validators=validators,choices=[data for data in parse_data_fk(fk_table,fk_data)],default=preview_data.id)
                    del fk_list
                else:
                    input_obj = IntegerField(label=k)
                
                inputs[k] = input_obj
                UpdateDataForm.values[k] = controller_get_attr(Config.MODELS_CRUD.get(tablename),instance_id,k)
        for k,v in inputs.items():
            setattr(UpdateDataForm,k,v)
        return UpdateDataForm()
    
class CustomAddForm:
    def generate_input(table_types:dict,tablename):
        class AddDataForm(FlaskForm):
            pass
        inputs = {}
        for k,v in table_types.items():
            if type(v[0]) == type(String()):
                validators = []
                if not v[1].nullable:
                    validators.append(DataRequired())
                if getattr(v[0],"length",None):
                    validators.append(Length(0,v[0].length))
                    input_obj = StringField(label=k,validators=validators)
                else:   
                    input_obj = StringField(label=k,validators=validators)
                inputs[k] = input_obj
            elif type(v[0]) == type(Integer()):
                fk = v[1].foreign_keys.copy()
                fk_list = list(dict.fromkeys(get_foreign_tables(fk))).copy()[::-1]
                if len(fk_list) > 1:
                    fk = v[1].foreign_keys.copy()
                    fk_table= f"{fk.pop().column.table}"
                    fk_data = controller_get_fk_data(Config.MODELS_CRUD.get("type_service"))
                    input_obj = SelectField(id=get_foreign_tablename(fk_table),label=fk_table,render_kw={"onchange":"getWrapeSelect(this)"},validators=validators,choices=[(data[0],f'{data[1]}') for data in parse_data_fk(fk_list[0],fk_data)])
                else:
                    fk = v[1].foreign_keys.copy()
                    fk_table= f"{fk.pop().column.table}"
                    fk_data = controller_get_fk_data(Config.MODELS_CRUD.get(fk_table,None))
                    input_obj = SelectField(label=k,validators=validators,choices=[data for data in parse_data_fk(fk_table,fk_data)])
                inputs[k] = input_obj
            
        for k,v in inputs.items():
            setattr(AddDataForm,k,v)
        setattr(AddDataForm,"submit",SubmitField(label="add"))
        return AddDataForm()


            
