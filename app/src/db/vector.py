from pymilvus import MilvusClient
from app.src.initial import env


class VectorDB(object):
    """
    vector db
    """
    def __init__(self):
        self.client = MilvusClient(env.vector_db.VECTOR_CLIENT_NAME)
        self.__init_collection()

    def __init_collection(self):
        # Check if collection already exists
        if env.vector_db.COLLECTION_NAME not in self.client.list_collections():
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
        stats = self.client.get_collection_stats(env.vector_db.COLLECTION_NAME)
        return int(stats["row_count"])

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