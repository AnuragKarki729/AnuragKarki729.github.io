import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
from keras.utils import load_img, img_to_array
from ExtractNames import get_breed_name
import cv2
import os
import shutil
from collections import Counter


# Load the trained model
model = tf.keras.models.load_model('DogPredictionModel.keras')

# Define class names
class_names = get_breed_name()

def classify_image(image_path, return_prediction=False):
    img = load_img(image_path, target_size=(150, 150))
    img_array = img_to_array(img) / 255.0  # Normalize the image
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions)
    
    if return_prediction:
        return predicted_class, confidence
    else:
        result_label.config(text=f"Predicted: {class_names[predicted_class]} \nConfidence: {confidence:.2f}")


def classify_video(video_path):
    if os.path.exists("video_frames"):
        shutil.rmtree("video_frames")
    os.makedirs("video_frames")

    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    success = True
    
    predictions_list = []

    while success:
        success, frame = cap.read()
        if success and count % int(frame_rate) == 0:  
            
            resized_frame = cv2.resize(frame, (150, 150))
            
            frame_path = f"video_frames/frame_{count}.jpg"
            cv2.imwrite(frame_path, resized_frame)
            
            predicted_class, confidence = classify_image(frame_path, return_prediction=True)
            predictions_list.append(predicted_class)
            
            display_frame(resized_frame)
            window.update()
            

        count += 1
    
    majority_class = Counter(predictions_list).most_common(1)[0][0]
    result_label.config(text=f"Majority Class: {class_names[majority_class]}")
    
    cap.release()
    shutil.rmtree("video_frames")


# Function to open the file dialog and load the image
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    if file_path:
        img = Image.open(file_path)
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        img_label.image = img_tk
        
        classify_image(file_path)
        
def open_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if file_path:
        classify_video(file_path)
        
def display_frame(frame):
    # Convert the OpenCV frame (BGR) to RGB format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the frame to a PIL Image
    img = Image.fromarray(frame_rgb)

    # Resize for display in GUI (if needed)
    img = img.resize((200, 200))

    # Convert to ImageTk format for displaying in tkinter
    img_tk = ImageTk.PhotoImage(img)

    # Update the GUI label to show the frame
    img_label.config(image=img_tk)
    img_label.image = img_tk

# Set up the GUI window
window = tk.Tk()
window.title("Dog Breed Classifier")

# Upload button
upload_image_button = tk.Button(window, text="Upload Image", command=open_image)
upload_image_button.pack(pady=10)


# Classification result label
upload_video_button = tk.Button(window, text="Upload Video", command=open_video)
upload_video_button.pack(pady=10)

# Image display label
img_label = tk.Label(window)
img_label.pack(pady=10)

result_label = tk.Label(window, text="Upload an image or video to classify", font=("Helvetica", 16))
result_label.pack(pady=10)

# Start the GUI loop
window.mainloop()