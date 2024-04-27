def controller_get_data_by_fk(crud_model,fk_id):
    data = crud_model.get_data_by_fk(fk_id)
    return data

def generate_select_title_service_html(parent_id):
    from app.system_db.title_service import TitleServiceCRUD
    html_list = '<select id="title_service_id" name="wrape_select" required onchange="getWrapeSelectService(this)">'
    data = controller_get_data_by_fk(TitleServiceCRUD,parent_id)
    for i in range(len(data)):
        if i == 0:wrape_id = data[i].id
        option = f"<option value='{data[i].id}'>{data[i].title_service}</option>"
        html_list = f"{html_list}{option}"
    html_list = f"{html_list}</select>"

    wrape_data = generate_select_service_html(wrape_id)
    return html_list,wrape_data 

def generate_select_service_html(parent_id):
    from app.system_db.service import ServiceCRUD
    html_list = '<select id="service_id" name="wrape_select_service" required>'
    for elem in ServiceCRUD.get_fk_data(parent_id):
        option = f"<option value='{elem.id}'>{elem.service}</option>"
        html_list = f"{html_list}{option}"
    html_list = f"{html_list}</select>"
    return html_list