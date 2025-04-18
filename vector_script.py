import os
import numpy as np
from PIL import Image
from app.src.initial import env, CV_MODEL, VectorDB
from app.src.third_api.pcc_images import check_and_create_directory, get_pcc_images, write_to_directory


def prepare_images():
    """
    prepare images
    :return:
    """
    total_data = []
    for page in range(1, 100):
        records = get_pcc_images(page)["records"]
        if not records:
            break
        total_data.extend(records)
    write_to_directory(total_data)


def prepare_vector_db():
    """
    prepare vector db
    :return:
    """
    all_data = []
    for _id, name in enumerate(os.listdir(env.model.PCC_IMAGE_DIR)):
        if _id % 10 == 0:
            print(_id)
        image_path = os.path.join(env.model.PCC_IMAGE_DIR, name)
        image = Image.open(image_path)
        image_np = np.array(image)
        features = CV_MODEL.predict(image_np)
        product_id = name.split(".")[0]
        all_data.append({
            "id": _id,
            "product_id": product_id,
            "vector": features
        })

    with VectorDB() as vector_db:
        vector_db.insert_db(all_data)


if __name__ == "__main__":
    # check_and_create_directory()
    # if os.path.exists(env.vector_db.VECTOR_CLIENT_NAME):
    #     os.remove(env.vector_db.VECTOR_CLIENT_NAME)
    prepare_images()
    prepare_vector_db()
