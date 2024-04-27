from config import Config

def controller_preview_data(crud_model,page):
    preview_data = crud_model.get_preview_data(offset=page)
    return preview_data

def controller_get_types(crud_model):
    return crud_model.get_types()

def controller_update(crud_model,id,params):
    crud_model.update(id=id,**params)

def controller_add(crud_model,params):
    crud_model.add(**params)

def controller_get_attr(crud_model,instance_id,attr_name):
    return getattr(crud_model.get(instance_id),attr_name,None)

def controller_get_fk_data(crud_model):
    return crud_model.get_fk_data()

def controller_get_crud_model(tablenames:list):
    for tablename in tablenames:
        if tablename != "type_service":
            yield Config.MODELS_CRUD.get(tablename)
        else:
            continue



def controller_get_fk_preview(crud_models,last_crud_model,id,tablenames,tablename):
    if "title_service" in tablenames and tablename != "title_service":
        tablenames[0] = "service"

    if len(crud_models) > 1:
        for i in range(len(crud_models)):
            print(tablenames[i],crud_models)
            if tablenames[i] != "type_service":
                
                if i == 0:
                    fk_id = crud_models[i].get_fk_id(id)
                    continue
                
                try: 
                    fk_id = crud_models[i].get_fk_id(fk_id)
                except UnboundLocalError:
                    fk_id = crud_models[i].get_fk_id(id)
    else:
        print(tablenames)
        if tablenames[0] == "type_service":
            fk_id = crud_models[0].get_fk_id(id)
            return last_crud_model.get(fk_id)

    return last_crud_model.get(fk_id)

    

def parse_data_fk(tablename,obj):
    for data in obj:
        id = data.id
        yield (id,data.type_service)

def controller_delete(crud_model,id):
    crud_model.delete(id)

def get_foreign_tables(fk_obj,fk_tables:list=[]):
    while True:
        try:
            fk_tables.append(str(fk_obj.copy().pop().column.table))
            fk_obj = list(fk_obj.pop().column.table.foreign_keys)
            return get_foreign_tables(fk_obj=fk_obj,fk_tables=fk_tables)
        except IndexError:
            return fk_tables
        except KeyError:
            return []
    

def get_wrpe_options(options_list:list,tablename):
    for data in options_list:
        id = data.id
        if tablename == "service":
            data = data.service
        yield (id,data)

def controller_get_data_by_fk(crud_model,fk_id):
    data = crud_model.get_data_by_fk(fk_id)
    return data

def get_foreign_tablename(tablename):
    if tablename == 'title_service':
        fk_table = "type_service"
    elif tablename == "type_service":
        fk_table = "title"
    return fk_table

def generate_select_html(parent_id,tablename):
    if tablename == 'service':
        from app.system_db.title_service import TitleServiceCRUD
        from app.admin.controller import controller_get_data_by_fk
        html_list = '<select id="title_service_id" name="wrape_select" required onchange="wrapeSelect(this)">'
        for elem in controller_get_data_by_fk(TitleServiceCRUD,parent_id):
            option = f"<option value='{elem.id}'>{elem.title_service}</option>"
            html_list = f"{html_list}{option}"
        html_list = f"{html_list}</select>"
        return html_list
    

def controller_get_other_data(tablename,crud_model,id):
    if tablename == "users":
        return crud_model.get_phone(id)