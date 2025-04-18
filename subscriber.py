import redis
import requests
from PIL import Image
from io import BytesIO
from app.src.initial import CV_MODEL, VectorDB
import numpy as np 
import logging



def subscribe_image(image_url):
    # 获取图片
    response = requests.get(image_url)
    # 用 PIL 打开图片并转换为 RGB
    image = Image.open(BytesIO(response.content)).convert("RGB")
    # 转换为 numpy 数组
    image_np = np.array(image)
    # 转换为图片
    features = CV_MODEL.predict(image_np)
    return features


def main():
    # 连接 Redis 服务器
    r = redis.StrictRedis(
        host='10.10.15.97',  # 你的服务器 IP
        port=6380,           # 映射的本地端口
        password='redisTest123',
        decode_responses=True  # 自动解码为字符串
    )

    # 创建 pubsub 对象并订阅频道
    pubsub = r.pubsub()
    pubsub.subscribe('my-channel-product-images')  # 可以换成你自己的频道名

    print("✅ 已订阅 'my-channel-product-images'，等待消息...")

    # 消费消息
    for message in pubsub.listen():
        try:
            image_url = message["data"]["url"]
            product_id = message["data"]["product_id"]

        except Exception as e:
            continue
        
        try:
            with VectorDB() as vector_db:
                vector = subscribe_image(image_url)
                vector_db.insert_db([{"vector": vector, "product_id": product_id}])
        except Exception as e:
            logging.info(e)
            

if __name__ == '__main__':
    main()
