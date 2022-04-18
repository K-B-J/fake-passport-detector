import requests
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv

load_dotenv()


def upload_image(name, file):
    resp = requests.post(
        os.environ.get("IPFS_ENDPOINT") + "/api/v0/add", files={name: file}
    )
    ipfs_hash = resp.json()["Hash"]
    return ipfs_hash


def download_image(hash):
    resp = requests.post(os.environ.get("IPFS_ENDPOINT") + f"/api/v0/cat?arg={hash}")
    image_file = io.BytesIO(resp.content)
    image = Image.open(image_file)
    buf = io.BytesIO()
    image.save(buf, format="png")
    byte_im = buf.getvalue()
    print(type(byte_im))
    image_final = base64.b64encode(byte_im).decode("utf-8")
    return image_final
