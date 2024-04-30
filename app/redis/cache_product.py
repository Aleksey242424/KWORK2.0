from app.redis import redis_client

def add_product(product_id,product_title,product_price,product_photo,service,title_service):
    redis_client.lpush(f"product_{product_id}",product_id,product_title,product_price,product_photo,service,title_service)
    return

def update_product(product_id,product_title,product_price,service,title_service):
    product_photo = redis_client.lrange(f"product_{product_id}",0,-1)[3].decode("utf-8")
    redis_client.delete(f"product_{product_id}")
    add_product(product_id,product_title,product_price,product_photo,service,title_service)
