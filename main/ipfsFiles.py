import requests
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv

load_dotenv()


def upload_image(name, file):
    resp = requests.post(
        "https://api.web3.storage/upload",
        headers={"Authorization": "Bearer " + os.environ.get("IPFS_TOKEN")},
        data=file,
    )
    ipfs_hash = resp.json()["cid"]
    return ipfs_hash


def download_image(cid):
    resp = requests.get("https://dweb.link/ipfs/" + cid, allow_redirects=True)
    image_file = io.BytesIO(resp.content)
    image = Image.open(image_file)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    image_final = base64.b64encode(byte_im).decode("utf-8")
    return image_final
