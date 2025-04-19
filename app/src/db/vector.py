from pymilvus import MilvusClient
from app.src.initial import env
import time


class VectorDB(object):
    """
    vector db
    """
    def __init__(self):
        self.client = MilvusClient(uri="http://10.10.15.97:19530", token="root:Milvus")
        self.__init_collection()

    def __init_collection(self):
        self.client.create_collection(
            collection_name=env.vector_db.COLLECTION_NAME,
            dimension=env.vector_db.VECTOR_SIZE
        )

    def insert_db(self, data):
        """
        insert database
        :return:
        """
        self.client.insert(
            collection_name=env.vector_db.COLLECTION_NAME,
            data=data
        )

    def search_db(self, features):
        """
        search db
        :param features:
        :return:
        """
        return self.client.search(
            collection_name=env.vector_db.COLLECTION_NAME,
            data=features,
            limit=env.vector_db.TOP_K,
            output_fields=["product_id"]
        )
    
    def count_db(self):
        """
        return number of entities in the collection
        """
        try:
            # 使用 query 方法获取总数
            results = self.client.query(
                collection_name=env.vector_db.COLLECTION_NAME,
                output_fields=["count(*)"]
            )
            if results and len(results) > 0:
                return results[0]["count(*)"]
            return 0
        except Exception as e:
            print(f"获取记录数失败: {str(e)}")
            return 0

    def get_all_data(self, limit=100):
        """
        get all data from collection
        :param limit: maximum number of records to return
        :return: list of records
        """
        try:
            # 使用 query 方法获取数据
            results = self.client.query(
                collection_name=env.vector_db.COLLECTION_NAME,
                output_fields=["id", "product_id"],
                limit=limit
            )
            if not results:
                print("⚠️ 查询返回空结果")
            return results
        except Exception as e:
            print(f"获取数据失败: {str(e)}")
            return []

    def delete_all_data(self):
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
                collection_name=env.vector_db.COLLECTION_NAME,
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

    def __enter__(self):
        """
        Enter the context and return the current instance.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the connection when exiting the context.
        """
        if hasattr(self, 'client'):
            self.client.close()  # Close the connection