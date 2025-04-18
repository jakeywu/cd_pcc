# -*- coding: utf-8 -*-
# @Time    : 2024/12/12 16:40
# @Author  : Wu WanJie

from transformers import ViTImageProcessor, ViTModel
from app.src.initial import env
import torch


class LoadCVFeatureModel(object):
    """
    load cv feature model
    """
    def __init__(self):
        self.processor = ViTImageProcessor.from_pretrained(env.model.CV_FEATURE_MODEL_DIR)
        self.model = ViTModel.from_pretrained(env.model.CV_FEATURE_MODEL_DIR)

    def predict(self, image_np):
        """
        predict image feature
        :param image_np:
        :return:
        """
        inputs = self.processor(images=image_np, return_tensors="pt")
        # 推理
        with torch.no_grad():  # 禁用梯度计算
            outputs = self.model(**inputs)
            class_token_vector = outputs.last_hidden_state[:, 0, :]
            class_token_vector = class_token_vector.squeeze(0).numpy()
        return class_token_vector
