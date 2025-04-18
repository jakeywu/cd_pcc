import pydantic
from typing import Any
from pydantic import BaseModel
from fastapi import HTTPException


class BaseResponse(BaseModel):
    """
    base result
    """
    code: int = pydantic.Field(200, description="API status code")
    message: str = pydantic.Field("success", description="API status message")
    data: Any = pydantic.Field(None, description="API data")


def api_output(data: Any = None, message: str = "success", code: int = 200):
    """
    api output
    :param data:
    :param message:
    :param code:
    :return:
    """
    return BaseResponse(
        data=data,
        message=message.lower(),
        code=code,
    )


# Custom HTTPException for consistent response structure
class CustomHTTPException(HTTPException):
    """
    custom error
    """
    def __init__(self, code: int = 400, message: str = "Parameter error"):
        self.status_code = code
        self.detail = {"code": code, "message": message.lower(), "data": None}


def convert_search_result(search_result):
    """
    convert
    :param search_result:
    :return:
    """
    final_result = []
    for item in search_result:
        similarity = round(item["distance"], 3)
        product_id = item["entity"]["product_id"].split("_")[0]
        final_result.append(
            {
                "product_id": product_id,
                "similarity": similarity,
            }
        )
    return final_result
