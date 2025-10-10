from pymilvus import MilvusClient
from app.src.initial import env
import time
import logging
from typing import List, Dict, Any, Optional

# 设置日志
logger = logging.getLogger(__name__)

class VectorDB:
    """
    向量数据库操作类
    """
    def __init__(self, db_path: str = None):
        """
        初始化 Milvus 客户端（本地模式）
        
        Args:
            db_path: 本地数据库文件路径
        """
        self.db_path = db_path or env.vector_db.VECTOR_CLIENT_NAME
        self.collection_name = env.vector_db.COLLECTION_NAME
        self.vector_size = env.vector_db.VECTOR_SIZE
        
        try:
            # 使用本地文件模式
            self.client = MilvusClient(uri=self.db_path)
            self.__init_collection()
            logger.info(f"成功连接到本地向量数据库: {self.db_path}")
        except Exception as e:
            logger.error(f"连接本地向量数据库失败: {str(e)}")
            raise
    def __init_collection(self):
        """初始化集合"""
        try:
            # 检查集合是否已存在
            if not self.client.has_collection(self.collection_name):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    dimension=self.vector_size
                )
                logger.info(f"创建集合: {self.collection_name}, 维度: {self.vector_size}")
            else:
                # 验证现有集合的维度是否匹配
                collection_info = self.client.describe_collection(self.collection_name)
                
                # 正确获取向量维度：从 fields 中的向量字段获取
                existing_dim = None
                for field in collection_info.get('fields', []):
                    if field.get('type') == 101:  # 101 表示 FLOAT_VECTOR
                        existing_dim = field.get('params', {}).get('dim')
                        break
                
                print(f"现有集合维度: {existing_dim}, 配置维度: {self.vector_size}")
                
                if existing_dim is None:
                    logger.warning("无法获取现有集合的向量维度")
                    # 删除并重新创建集合
                    self.client.drop_collection(self.collection_name)
                    self.client.create_collection(
                        collection_name=self.collection_name,
                        dimension=self.vector_size
                    )
                    logger.info(f"重新创建集合: {self.collection_name}, 维度: {self.vector_size}")
                elif existing_dim != self.vector_size:
                    logger.warning(f"集合维度不匹配: 现有{existing_dim} vs 配置{self.vector_size}")
                    logger.info("删除现有集合并重新创建...")
                    
                    # 删除现有集合
                    self.client.drop_collection(self.collection_name)
                    
                    # 重新创建集合
                    self.client.create_collection(
                        collection_name=self.collection_name,
                        dimension=self.vector_size
                    )
                    logger.info(f"重新创建集合: {self.collection_name}, 维度: {self.vector_size}")
                else:
                    logger.info(f"集合已存在: {self.collection_name}, 维度匹配: {existing_dim}")
        except Exception as e:
            logger.error(f"初始化集合失败: {str(e)}")
            raise

    def insert_db(self, data: List[Dict[str, Any]]) -> bool:
        """
        insert database
        :return:
        """
        try:
            if not data:
                logger.warning("插入数据为空")
                return False
                
            self.client.insert(
                collection_name=self.collection_name,
                data=data
            )
            logger.info(f"成功插入 {len(data)} 条数据")
            return True
        except Exception as e:
            logger.error(f"插入数据失败: {str(e)}")
            return False

    def search_db(self, features: List[List[float]]) -> List[List[Dict]]:
        """
        search db
        :param features:
        :return:
        """
        try:
            if not features:
                logger.warning("搜索向量为空")
                return []
                
            results = self.client.search(
                collection_name=self.collection_name,
                data=features,
                limit=env.vector_db.TOP_K,
                output_fields=["product_id"]
            )
            return results
        except Exception as e:
            logger.error(f"搜索失败: {str(e)}")
            return []

    def count_db(self) -> int:
        """
        return number of entities in the collection
        """
        try:
            # 使用 query 方法获取总数
            results = self.client.query(
                collection_name=self.collection_name,
                output_fields=["count(*)"],
                limit=1
            )
            if results and len(results) > 0:
                return results[0]["count(*)"]
            return 0
        except Exception as e:
            print(f"获取记录数失败: {str(e)}")
            return 0

    def get_all_data(self, limit: int = 100) -> List[Dict]:
        """
        get all data from collection
        :param limit: maximum number of records to return
        :return: list of records
        """
        try:
            # 使用 query 方法获取数据
            results = self.client.query(
                collection_name=self.collection_name,
                output_fields=["id", "product_id"],
                limit=limit
            )
            if not results:
                print("⚠️ 查询返回空结果")
            return results
        except Exception as e:
            print(f"获取数据失败: {str(e)}")
            return []

    def delete_all_data(self) -> bool:
        """
        delete all data from collection
        :return: True if successful, False otherwise
        """
        try:
            # 获取当前记录数
            initial_count = self.count_db()
            print(f"删除前记录数: {initial_count}")
            
            if initial_count == 0:
                print("集合中已经没有数据")
                return True
                
            # 删除所有数据
            self.client.delete(
                collection_name=self.collection_name,
                filter="id >= 0"  # 删除所有记录
            )
            
            # 等待删除操作完成
            time.sleep(1)
            
            # 验证删除结果
            final_count = self.count_db()
            print(f"删除后记录数: {final_count}")
            
            if final_count == 0:
                print("✅ 成功删除所有数据")
                return True
            else:
                print(f"⚠️ 删除操作可能未完成，当前记录数: {final_count}")
                return False
                
        except Exception as e:
            print(f"删除数据失败: {str(e)}")
            return False

    def close(self):
        """关闭连接"""
        if hasattr(self, 'client'):
            self.client.close()
            logger.info("向量数据库连接已关闭")

    def __enter__(self):
        """
        Enter the context and return the current instance.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the connection when exiting the context.
        """
        self.close()


# 单例模式
class VectorDBManager:
    """
    VectorDB 管理器，提供单例访问
    """
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'VectorDB':
        if cls._instance is None:
            cls._instance = VectorDB()
        return cls._instance
    
    @classmethod
    def close_instance(cls):
        if cls._instance is not None:
            cls._instance.close()
            cls._instance = None


# 保持原有变量名不变
Milvus_Client_VectorDB = VectorDBManager.get_instance()