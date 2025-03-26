import os
import logging
import numpy as np
import imageio.v3 as imageio
import scipy.ndimage
import cv2

def rgb2gray(image):
    return np.dot(image[..., :3].astype(np.float32), [0.2989, 0.5870, 0.1140]).astype(np.uint8)

def convert(front, back):
    denominator = 255.0 - back.astype(np.float32)
    np.maximum(denominator, 1.0, out=denominator)  # Avoid division by zero
    final = np.multiply(front, 255.0, dtype=np.float32) / denominator
    np.clip(final, 0, 255, out=final)
    final[back == 255] = 255  # Preserve white areas
    return final.astype(np.uint8)

def enhance_sketch(sketch, gray):
    # Increase contrast using CLAHE (adaptive histogram equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_sketch = clahe.apply(sketch)

    # Blend with original grayscale to restore details
    alpha = 0.7  # Stronger sketch weight
    beta = 0.3   # Lighter grayscale blend
    blended = cv2.addWeighted(enhanced_sketch, alpha, gray, beta, 0)

    return blended

def process_image(input_path):
    try:
        # Load image
        image = imageio.imread(input_path)

        # Convert to grayscale
        gray = rgb2gray(image)

        # Invert grayscale
        inverted = 255 - gray

        # Adjust blur dynamically based on image size
        blur_intensity = max(image.shape[:2]) / 50  # Scales blur to image size
        blur = scipy.ndimage.gaussian_filter(inverted.astype(np.float32), sigma=blur_intensity)

        # Generate initial sketch
        sketch = convert(blur, gray)

        # Darken and refine sketch
        final_sketch = enhance_sketch(sketch, gray)

        # Save the output as 'final_image.jpg'
        output_filename = "final_sketch.jpeg"
        output_path = os.path.join(os.getcwd(), output_filename)
        cv2.imwrite(output_path, final_sketch)

        logging.info(f"Sketch saved at: {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        raise

def main():
    input_path = "image.jpg"

    if not os.path.isfile(input_path):
        print(f"Error: File '{input_path}' not found!")
        return

    try:
        # Process the image and get output path
        output_path = process_image(input_path)
        print(f"Sketch created successfully! Saved at: {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
