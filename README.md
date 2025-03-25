# 🖼️ Image to Sketch

This project converts an RGB image into a pencil sketch using a series of image processing techniques. The process includes grayscale conversion, negative image creation, Gaussian blur application, and color dodge blending to achieve the sketch effect.

---

## 📚 Features
- Converts any RGB image into a pencil sketch.
- Smooth sketch effect with fine details.
- Quick and efficient image processing using OpenCV and NumPy.
- Saves the generated sketch as an output file.

---

## 🛠️ Technologies Used
- Python 3.x
- OpenCV
- NumPy
- Matplotlib (Optional, for visualization)



---

## 🚀 Getting Started
Follow these steps to run the project on your local machine:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/officialayushyadav15/image_to_sketch.git
cd image_to_sketch
```

### 2️⃣ Install Dependencies
Run the following command to install all required libraries:
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Script
Run the main Python script to convert the image to a sketch:
```bash
python image_to_sketch.py
```

---

## 📝 How It Works
The image-to-sketch conversion follows these steps:

1. **Load RGB Image:** Read the original image.
2. **Convert to Grayscale:** Convert the image to grayscale for further processing.
3. **Create Negative Image:** Invert the grayscale image to create a negative.
4. **Apply Gaussian Blur:** Smooth the negative image using Gaussian blur.
5. **Color Dodge Blending:** Combine the grayscale image with the blurred negative using color dodge to create the sketch effect.
6. **Save Output:** Save the final sketch as `final_sketch.jpeg`.

---

## 📸 Sample Output
| Original Image | Sketch Output |
|----------------|----------------|
| ![Original](image.jpeg) | ![Sketch](final_sketch.jpeg) |

---

## 📄 Requirements
Ensure that you have the following libraries installed:
- OpenCV
- NumPy
- Matplotlib (Optional for visualization)

If not already installed, run:
```bash
pip install -r requirements.txt
```

---

## ⚡ Usage
- Place the input image in the `images` folder.
- Modify the file name in `image_to_sketch.py` if required.
- Run the script to generate the sketch.

---

## 🧩 Customization
- **Change Input File:** Edit the image path in the script.
- **Adjust Blur Intensity:** Modify the Gaussian blur parameters to control the sketch’s smoothness.
- **Tune Color Dodge Effect:** Adjust the blending to refine the sketch effect.

---

## 🐞 Troubleshooting
- Ensure that the image path is correct.
- Check that all required dependencies are installed.

---

## 📧 Contact
Feel free to reach out for support or suggestions:
- GitHub: [officialayushyadav15](https://github.com/officialayushyadav15)


---

✅ **Happy Sketching!** 🎨

