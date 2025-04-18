import requests
import mimetypes
image_path = "/Users/wujakey/Downloads/1.png"

with open(image_path, "rb") as f:
    image_data = f.read()

# 自动获取 MIME 类型
mime_type, _ = mimetypes.guess_type(image_path)

files = {
    "image": ("image.jpg", image_data, mime_type)
}
url = "http://127.0.0.1:8083/api/pcc/image/quality_check"
response = requests.post(url, files=files)
print(response.json())
