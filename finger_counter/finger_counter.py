''' Written by jared.vasquez@yale.edu '''

from keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
import copy
import cv2
import os
from skimage import transform


class FingerCounter:

    def __init__(self, model='model_6cat.h5'):

        self._model = load_model(model)
        self._classes = [None, 1, 2, 3, 4, 5]

    def _binary_mask(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = np.uint8(img)
        img = cv2.GaussianBlur(img, (7,7), 3)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        ret, new = cv2.threshold(img, 25, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return new

    def count(self, img):
        y0 = 100
        x0 = 100
        width = 300
        print('before', img.shape)
        img = img[y0:y0+width,x0:x0+width]
        img = self._binary_mask(img)
        img = np.float32(img) / 255 # Normalize
        # img = transform.resize(img, output_shape=(300, 300), mode='reflect')
        img = np.expand_dims(img, axis=0)
        img = np.expand_dims(img, axis=-1)
        print('after', img.shape)
        print(img[1:-1].shape)
        cv2.imshow("WINDOW 3", img[0,...,0])
        pred = self._classes[np.argmax(self._model.predict(img)[0])]
        return pred
