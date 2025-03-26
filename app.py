import os
import uuid
import logging
import numpy as np
import imageio.v3 as imageio
import scipy.ndimage
import cv2
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# Flask app setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def rgb2gray(image):
    """Convert RGB image to grayscale."""
    return np.dot(image[..., :3].astype(np.float32), [0.2989, 0.5870, 0.1140]).astype(np.uint8)

def convert(front, back):
    """Apply division-based sketch transformation with enhanced contrast."""
    denominator = 255.0 - back.astype(np.float32)
    np.maximum(denominator, 1.0, out=denominator)  # Avoid division by zero
    final = np.multiply(front, 255.0, dtype=np.float32) / denominator
    np.clip(final, 0, 255, out=final)
    final[back == 255] = 255  # Preserve white areas
    return final.astype(np.uint8)

def enhance_sketch(sketch, gray):
    """Blend the sketch with the original grayscale and enhance contrast."""
    
    # Increase contrast using CLAHE (adaptive histogram equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_sketch = clahe.apply(sketch)

    # Blend with original grayscale to restore details
    alpha = 0.7  # Stronger sketch weight
    beta = 0.3   # Lighter grayscale blend
    blended = cv2.addWeighted(enhanced_sketch, alpha, gray, beta, 0)

    return blended

def process_image(input_path):
    """Processes an image and returns the filename of the output sketch."""
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

        # Generate unique filename for processed image
        output_filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
        cv2.imwrite(output_path, final_sketch)

        return output_filename
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        raise

@app.route('/process', methods=['POST'])
def process():
    """Handles image upload and processing."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg'}), 400

    try:
        # Secure filename with UUID
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # Process image
        output_filename = process_image(input_path)
        return jsonify({'result_url': f"/processed/{output_filename}"})
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/')
def index():
    """Renders the main upload page."""
    return render_template('index.html')

@app.route('/processed/<filename>')
def processed_file(filename):
    """Serves the processed image."""
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
