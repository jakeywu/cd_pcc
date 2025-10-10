import redis
import requests
from PIL import Image
from io import BytesIO
from app.src.initial import CV_MODEL
from app.src.db.vector import Milvus_Client_VectorDB
import numpy as np 
import logging
import json
import os
from app.src.initial import env
from datetime import datetime


def subscribe_image(image_url, save_dir):
    # 验证图片URL后缀
    valid_extensions = {'.jpg', '.jpeg', '.png'}
    file_ext = os.path.splitext(image_url.split('?')[0])[1].lower()
    
    if file_ext not in valid_extensions:
        raise ValueError(f"不支持的图片格式: {file_ext}，支持的格式为: {valid_extensions}")
    
    # 获取图片
    response = requests.get(image_url)
    
    # 保存图片
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{os.path.basename(image_url.split('?')[0])}"
    save_path = os.path.join(save_dir, filename)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"图片已保存到: {save_path}")
    
    # 用 PIL 打开图片并转换为 RGB
    image = Image.open(BytesIO(response.content)).convert("RGB")
    # 转换为 numpy 数组
    image_np = np.array(image)
    # 转换为图片
    features = CV_MODEL.predict(image_np)
    return features


def sub_main():
    # 创建保存图片的目录
    save_dir = env.product.REDIS_PRODUCT_IMAGE_DIR
    os.makedirs(save_dir, exist_ok=True)
    print(f"图片将保存到目录: {save_dir}")

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

    start_id = 1000
    # 消费消息
    for message in pubsub.listen():
        if message['type'] != 'message':
            continue
            
        try:
            data = json.loads(message['data'])
            image_url = data["url"]
            product_id = data["product_id"]
            
            # 记录图片URL信息
            file_ext = os.path.splitext(image_url.split('?')[0])[1].lower()
            print(file_ext)
            print(f"处理图片: {product_id}, 格式: {file_ext}")
            vector = subscribe_image(image_url, save_dir)
            Milvus_Client_VectorDB.insert_db([{"id": start_id, "vector": vector, "product_id": product_id}])
            print(f"✅ 成功处理图片: {product_id}, 格式: {file_ext}")
            start_id += 1
                
        except Exception as e:
            logging.error(f"处理消息失败: {str(e)}")
            continue
