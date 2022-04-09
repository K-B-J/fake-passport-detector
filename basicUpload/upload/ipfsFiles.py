import requests
from PIL import Image
import io
import base64

def upload_image(name, file):
    resp = requests.post("http://127.0.0.1:5001/api/v0/add", files={name: file})
    ipfs_hash=resp.json()["Hash"]
    return ipfs_hash
def download_image():
    print("Hello")
    resp = requests.post("http://127.0.0.1:5001/api/v0/cat?arg=QmR7MvAVHsnfnMXUtSVU375uSBoFV2dX1zqNid8j2DtQbT")
    image_file = io.BytesIO(resp.content)
    image = Image.open(image_file)
    buf = io.BytesIO()
    image.save(buf, format='png')
    byte_im = buf.getvalue()
    print(type(byte_im))
    image_final = base64.b64encode(byte_im).decode('utf-8')
    return image_final