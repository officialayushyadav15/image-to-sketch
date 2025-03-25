import numpy as np
import imageio
import scipy.ndimage
import cv2

img = "image.jpg"

def rgb2gray(s):
    # Optimized grayscale conversion using matrix multiplication with pre-calculated weights
    return np.dot(s[..., :3].astype(np.float32), [0.2989, 0.5870, 0.1140])

def convert(front, back):
    # Vectorized operations with safe division and optimized clipping
    denominator = 255.0 - back.astype(np.float32)
    np.maximum(denominator, 1.0, out=denominator)  # Prevent division by zero
    final = np.multiply(front, 255.0, dtype=np.float32) / denominator
    np.clip(final, 0, 255, out=final)
    final[back == 255] = 255  # Preserve white areas
    return final.astype(np.uint8)


s = imageio.imread(img)
gray = rgb2gray(s).astype(np.uint8)
i = 255 - gray

blur = scipy.ndimage.gaussian_filter(i.astype(np.float32), sigma=30)

r = convert(blur, gray)
cv2.imwrite('final_sketch.jpeg', r)