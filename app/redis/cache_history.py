from app.redis import redis_client

def add_product_in_history(product_id,customer_id):
    redis_client.lrem(f"customer_{customer_id}",1,product_id)
    redis_client.lpush(f"customer_{customer_id}",product_id)

def get_history(customer_id):
    list_products_id = [id.decode("utf-8") for id in redis_client.lrange(f"customer_{customer_id}",0,-1)]
    list_products = [[data.decode("utf-8") for data in redis_client.lrange(f"product_{product_id}",0,-1)] for product_id in list_products_id]
    return list_products