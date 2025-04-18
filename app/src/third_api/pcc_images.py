# -*- coding: utf-8 -*-
# @Time    : 2025/1/18 09:04
# @Author  : Wu WanJie

import os
import shutil
import requests
from app.src.initial import env
from app.src.settings.c_logger import logger
import datetime

HEADERS = {
    'X-Internal-Service-Key': 'image-insight-internal-service-2024'
}


def get_pcc_images(page):
    """
    get pcc images
    :return:
    """
    end_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    try:
        response = requests.get(
            url=f'http://{env.product.PCC_PRODUCT_HOST}:{env.product.PCC_PRODUCT_PORT}{env.product.PCC_PRODUCT_ROUTE_IMAGE}',
            params={
                'start_time': '1900-01-01T00:00:00',
                'end_time': end_time,
                'exclude_market_circulation': True,
                'page': page,
                'page_size': 100,
            },
            headers=HEADERS
        )
    except Exception as e:
        logger.error(e)
        raise e

    datas = response.json()["data"]
    return datas


def check_and_create_directory():
    """
    check and create directory
    :return:
    """
    if os.path.exists(env.model.PCC_IMAGE_DIR):
        # 如果目录存在，删除该目录及其中的所有内容
        shutil.rmtree(env.model.PCC_IMAGE_DIR)

    # 创建新目录
    os.makedirs(env.model.PCC_IMAGE_DIR)


def write_to_directory(records):
    """
    write to directory
    """
    print(len(records))
    for i, record in enumerate(records):
        if i % 10 == 0:
            print(i)
        try:
            image_url = record["image_url"]
            response = requests.get(image_url)

        except Exception as e:
            logger.info(f"{record}下载失败，请重新下载")
            logger.error(e)
            continue
        with open(os.path.join(env.model.PCC_IMAGE_DIR, f"{record['product_id']}_{record['filename']}"), 'wb') as w_file:
            w_file.write(response.content)
