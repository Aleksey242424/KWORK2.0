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

    return html_list,wrape_data[0],wrape_data[1]

def generate_select_service_html(parent_id):
    from app.system_db.service import ServiceCRUD
    
    html_list = '<select id="wrape_select_service" name="wrape_select_service" required>'
    services = ServiceCRUD.get_fk_data(parent_id) 
    for i in range(len(services)):
        option = f"<option value='{services[i].id}'>{services[i].service}</option>"
        html_list = f"{html_list}{option}"
    html_list = f"{html_list}</select>"
    try:
        id = getattr(services[0],"id",None)
    except IndexError:
        id = None
    return html_list,id

def generate_product_by_price_and_service_html(service_id,start_price="",end_price=""):
    from app.system_db.product import ProductCRUD
    products = ProductCRUD.get_product_by_price_and_service(service_id=service_id,start_price=start_price,end_price=end_price)  
    product_html = ""
    list_data = []
    for product in products:
        list_data.append((product.id,product.photo))
        product_html = f"""{product_html}
                <a href='#' class='link'>
                        <div class="product_block">
                            <img src="#" width="300px" height="200px">
                        <div>
                            <p>{product.title}</p><br>
                            <p>цена: {product.price} ₽</p><br>
                        </div>
                    </div>
                </a>
            """
    product_html = f"<div>{product_html}</div>"
    return product_html,list_data