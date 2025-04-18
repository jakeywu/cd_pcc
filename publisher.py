import redis
import time

r = redis.StrictRedis(
    host='10.10.15.97',
    port=6380,
    password='redisTest123',
    decode_responses=True
)

channel = 'my-channel-product-images'
import json 
for i in range(10):
    message = f'消息 {i}'
    r.publish(channel, json.dumps({"url": "safsfsf", "product_id": "fsdf"}))
    print(f"✅ 发布消息: {message}")
    time.sleep(1)
