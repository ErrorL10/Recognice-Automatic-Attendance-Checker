import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import tkinter as tk

# Initialize the video capture device
cap = cv2.VideoCapture(0)  # 0 for default camera

# Declare the width and height in variables 
width, height = 800, 600
  
# Set the width and height 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 

# Define a function to capture and process frames
def process_frame():
    # Capture the current frame
    _, frame = cap.read()

    # Check if the frame was successfully captured
    # Decode the barcodes in the frame
    decoded_objects = decode_barcodes(frame)

    # Draw bounding boxes and data around detected barcodes
    for obj in decoded_objects:
        x, y, w, h = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, str(obj.data), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
    # Convert the processed frame to PIL Image format
    processed_image = Image.fromarray(frame)

    # Convert the PIL Image to Tkinter PhotoImage67
    photo_image = ImageTk.PhotoImage(image=processed_image)

    # Update the video label with the new frame
    label_widget.photo_image = photo_image 
    label_widget.configure(image=photo_image)
    label_widget.after(10, process_frame)


# Function to decode barcodes using brightness normalization
def decode_barcodes(frame):
    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Extract the V channel (brightness)
    brightness_channel = hsv_frame[:, :, 2]

    # Normalize the brightness channel
    normalized_brightness = cv2.normalize(brightness_channel, None, 0, 255, cv2.NORM_MINMAX)

    # Convert the normalized brightness back to BGR color space
    normalized_frame = cv2.cvtColor(normalized_brightness[:, :, None], cv2.COLOR_GRAY2BGR)

    # Decode the barcodes in the normalized frame
    decoded_objects = decode(normalized_frame)

    return decoded_objects

# Create the Tkinter GUI
root = tk.Tk()
root.title('Barcode Scanner')

# Create a label to display the video stream
label_widget = tk.Label(root)
label_widget.pack()

# Start the video capture loop
while True:
    process_frame()
    root.mainloop()
