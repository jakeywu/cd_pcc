# -*- coding: utf-8 -*-
# @Time    : 2024/12/12 17:49
# @Author  : Wu WanJie

from app.src.models.load_model import LoadCVFeatureModel
from app.src.db.vector import VectorDB
CV_MODEL = LoadCVFeatureModel()
Milvus_Client_VectorDB = VectorDB()