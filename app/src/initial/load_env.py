import os
from dotenv import load_dotenv

load_dotenv(override=True)


class LoadEnv:
    """
    env doc
    """
    def __init__(self):
        self.server = self.ServerConf(self)
        self.model = self.ModelConf(self)
        self.vector_db = self.VectorDBConf(self)
        self.product = self.ProductConf(self)

    class VectorDBConf:
        """
        vector db conf
        """
        def __init__(self, config):
            self.VECTOR_CLIENT_NAME = config.get_and_check_variable("VECTOR_CLIENT_NAME", str)
            self.VECTOR_SIZE = config.get_and_check_variable("VECTOR_SIZE", int)
            self.COLLECTION_NAME = config.get_and_check_variable("COLLECTION_NAME", str)
            self.TOP_K = config.get_and_check_variable("TOP_K", int)

    class ServerConf:
        """
        server config
        """
        def __init__(self, config):
            self.SERVER_HOST = config.get_and_check_variable("SERVER_HOST", str)
            self.SERVER_PORT = config.get_and_check_variable("SERVER_PORT", int)

    class ModelConf:
        """
        model config
        """
        def __init__(self, config):
            self.CV_FEATURE_MODEL_DIR = config.get_and_check_variable("CV_FEATURE_MODEL_DIR", str)
            self.PCC_IMAGE_DIR = config.get_and_check_variable("PCC_IMAGE_DIR", str)

    class ProductConf:
        """
        product config
        """
        def __init__(self, config):
            self.PCC_PRODUCT_HOST = config.get_and_check_variable("PCC_PRODUCT_HOST", str)
            self.PCC_PRODUCT_PORT = config.get_and_check_variable("PCC_PRODUCT_PORT", str)
            self.PCC_PRODUCT_ROUTE_IMAGE = config.get_and_check_variable("PCC_PRODUCT_ROUTE_IMAGE", str)
            self.REDIS_PRODUCT_IMAGE_DIR = config.get_and_check_variable("REDIS_PRODUCT_IMAGE_DIR", str)

    @staticmethod
    def get_and_check_variable(key, cast):
        """
        structure env
        :param key:  env key
        :param cast: key type
        :return:
        """
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Environment variable {key} is not set.")
        
        try:
            if cast is bool:
                return eval(value)
            return cast(value)
        except ValueError:
            raise ValueError(f"Environment variable {key}'s format is incorrect.")


env = LoadEnv()

if __name__ == "__main__":
    # 使用示例
    env_config = LoadEnv()
    print(env_config.server.SERVER_PORT)  # 获取OpenAI的模型名称
