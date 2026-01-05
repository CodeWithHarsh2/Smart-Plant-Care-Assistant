import cv2
import os
import numpy as np
from sklearn.metrics import accuracy_score

print("Starting Plant Stress Image Analysis")

IMAGE_DIR = "analysis/images"

images = []
labels = []

for label, folder in enumerate(["stressed", "healthy"]):
    folder_path = os.path.join(IMAGE_DIR, folder)
    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue
        img = cv2.resize(img, (128, 128))
        images.append(img)
        labels.append(label)

print("Total images:", len(images))


def extract_features(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    brightness = np.mean(hsv[:, :, 2])
    greenness = np.mean(hsv[:, :, 1])
    return brightness, greenness


features = [extract_features(img) for img in images]


def predict_health(b, g):
    if g > 80 and b > 80:
        return 1
    return 0


predictions = [predict_health(b, g) for b, g in features]
accuracy = accuracy_score(labels, predictions)

print("Accuracy:", accuracy)
