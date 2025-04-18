import redis
import time
import json
import uuid

r = redis.StrictRedis(
    host='10.10.15.97',
    port=6380,
    password='redisTest123',
    decode_responses=True
)

channel = 'my-channel-product-images'

for i in range(10):
    # 生成唯一的 product_id
    product_id = str(uuid.uuid4())
    
    message = {
        "url": "http://10.10.15.93:9000/product-images/9d1b57ce-e8e8-41d3-b5af-81a7ce186184_product2.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=mnsREH0gcF2oPReoPLeb%2F20250418%2F%2Fs3%2Faws4_request&X-Amz-Date=20250418T161039Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=7c8f97ee80849deace2c556aa8c595dc7f81781cd9ac8c73ac68d274b275c44e",
        "product_id": product_id
    }
    
    r.publish(channel, json.dumps(message))
    print(f"✅ 发布消息: {product_id}")
    time.sleep(1)
