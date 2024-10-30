import numpy as np
from feature import FeatureExtraction
url=input("Enter URL:")

def preprocess_url(url):
    feature_extractor = FeatureExtraction(url)
    features = feature_extractor.getFeaturesList()
    return np.array(features).reshape(1, -1)

features = preprocess_url(url)

print(features)
