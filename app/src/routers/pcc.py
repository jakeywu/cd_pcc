import io
from fastapi import APIRouter, UploadFile, File
from app.src.settings.c_logger import logger
from app.src.utils.output import api_output, CustomHTTPException, convert_search_result
from PIL import Image
import numpy as np
from app.src.initial import Milvus_Client_VectorDB, CV_MODEL


pcc_router = APIRouter()


@pcc_router.post("/classfication")
async def extract_feature(file: UploadFile = File(...)):
    """
    接收一张图片并提取其特征向量
    :param file: 上传的图片文件
    :return: 图片特征向量
    """
    try:
        # 确保文件是图片类型
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise CustomHTTPException(message="Unsupported file type. Please upload a JPEG or PNG image.")

        # 读取文件内容并转为 NumPy 数组
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image)  # 将 Pillow Image 转换为 NumPy 数组

        # 检查图像是否有 alpha 通道，若有则移除
        if image_np.shape[-1] == 4:  # 检查是否为 RGBA 格式
            image_np = image_np[..., :3]  # 去掉 alpha 通道

        features = CV_MODEL.predict(image_np)
        
        search_result = Milvus_Client_VectorDB.search_db([features])[0]
        final_result = convert_search_result(search_result)
        return api_output(data=final_result)
    except Exception as e:
        raise CustomHTTPException(message=f"Error processing image: {str(e)}")


# 需要登录后才能访问的接口
@pcc_router.post("/quality_check")
async def image_quality_check(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        logger.info(image.content_type)
        return api_output(data=True)
    except Exception as e:
        raise CustomHTTPException(code=500, message=f"Error reading image: {str(e)}")



# 需要登录后才能访问的接口
@pcc_router.post("/sync_images")
async def synchronize_images(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        logger.info(image.content_type)
        return api_output(data=True)
    except Exception as e:
        raise CustomHTTPException(code=500, message=f"Error reading image: {str(e)}")
