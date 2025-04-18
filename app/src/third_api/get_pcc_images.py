# -*- coding: utf-8 -*-
# @Time    : 2025/1/18 09:04
# @Author  : Wu WanJie

import os
import requests
from app.src.initial import env
from app.src.settings.c_logger import logger
import datetime

HEADERS = {
    'X-Internal-Service-Key': 'image-insight-internal-service-2024'
}


def get_pcc_images():
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
                'exclude_market_circulation': True
            },
            headers=HEADERS
        )
    except Exception as e:
        logger.error(e)
        raise e

    datas = response.json()["data"]
    return datas


def write_to_directory(datas):
    """
    write to directory
    """
    records = datas["records"]
    for i, record in enumerate(records):
        try:
            response = requests.get(record["image_url"])
        except Exception as e:
            logger.info(f"{record}下载失败，请重新下载")
            logger.error(e)
            continue

        with open(os.path.join(env.model.PCC_IMAGE_DI, f"{record['product_id']}_{i}"), 'wb') as w_file:
            w_file.write(response.content)
