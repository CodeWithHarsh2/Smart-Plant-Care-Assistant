import os
from PIL import Image
import numpy as np

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_image(file_storage, filename=None):
    """Save an uploaded image and return path."""
    if filename is None:
        filename = file_storage.filename
    path = os.path.join(UPLOAD_FOLDER, filename)
    file_storage.save(path)
    return path

def open_image_to_array(path):
    img = Image.open(path).convert('RGB')
    arr = np.array(img)
    return img, arr

# Simple helper to compute percent yellowing
def yellow_ratio(arr):
    # arr expected uint8 HxWx3
    r = arr[:, :, 0].astype(int)
    g = arr[:, :, 1].astype(int)
    b = arr[:, :, 2].astype(int)
    # heuristic: strongly yellow pixels: r and g high, b lower
    yellow_mask = (r > 150) & (g > 140) & (b < 120)
    ratio = yellow_mask.sum() / (arr.shape[0] * arr.shape[1])
    return float(ratio)

# Brown/spot detection heuristic
def brown_spot_ratio(arr):
    r = arr[:, :, 0].astype(int)
    g = arr[:, :, 1].astype(int)
    b = arr[:, :, 2].astype(int)
    # dark brown-ish: r medium, g lower, b lower
    brown = (r > 90) & (r < 200) & (g < 120) & (b < 100)
    return float(brown.sum() / (arr.shape[0] * arr.shape[1]))
