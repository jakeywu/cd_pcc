from pymilvus import MilvusClient, DataType
from app.src.initial import env


class VectorDB(object):
    """
    vector db
    """
    def __init__(self):
        self.client = MilvusClient(env.vector_db.VECTOR_CLIENT_NAME)
        self.__init_collection()

    def __init_collection(self):
        schema = MilvusClient.create_schema(
            auto_id=False,
            enable_dynamic_field=False
        )
        schema.add_field("id", DataType.INT64, is_primary=True)
        schema.add_field("product_id", DataType.VARCHAR, max_length=100)
        schema.add_field("vector", DataType.FLOAT_VECTOR, dim=env.vector_db.VECTOR_SIZE)

        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name="vector",
            index_type="HNSW",  # Using HNSW instead of IVF_FLAT for local mode
            metric_type="L2",   # or "IP" depending on your needs
            params={
                "M": 16,       # HNSW specific parameter
                "efConstruction": 200
            }
        )

        self.client.create_collection(
            collection_name=env.vector_db.COLLECTION_NAME,
            schema=schema,
            index_params=index_params
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
        search_params = {
            "metric_type": "L2",  # Must match the metric type used in index creation
            "params": {"ef": 50}  # HNSW search parameter
        }
        
        return self.client.search(
            collection_name=env.vector_db.COLLECTION_NAME,
            data=features,
            limit=env.vector_db.TOP_K,
            output_fields=["product_id"],
            search_params=search_params
        )
    
    def count_db(self):
        """
        return number of entities in the collection
        """
        stats = self.client.get_collection_stats(env.vector_db.COLLECTION_NAME)
        return int(stats["row_count"])