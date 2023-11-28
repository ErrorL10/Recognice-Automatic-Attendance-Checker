import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import tkinter as tk
import customtkinter as ctk

class barcode_window(tk.Toplevel):
    def __init__(self):
        super().__init__()
        
        self.title('Barcode Scanner')
        self.geometry('900x600')
        
        self.camera_frame = camera_frame(master=self)
        self.camera_frame.pack() 

class camera_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.camera_panel = ctk.CTkFrame(master=self)
        self.camera_panel.grid(row=0, column=0, sticky='nesw')
        
        self.camera = ctk.CTkLabel(master=self.camera_panel, text="")
        self.camera.grid(row=0, column=0, padx=20, pady=20, sticky='nesw')
        self.open_camera_button = ctk.CTkButton(master=self.camera_panel, text="Open Camera", command=self.open_camera)
        self.open_camera_button.grid(row=1, column=0, padx=20, pady=20, sticky='nesw')
        
        self.info_frame = ctk.CTkFrame(master=self)
        self.info_frame.grid(row=0, column=1, sticky='nesw')
        
        #Present Students List
        self.students_list = tk.Listbox(master=self.info_frame)
        self.students_list.grid(row=0, column=0, padx=20, pady=20, sticky='nesw')
        
        #Next Button
        self.finish_button = ctk.CTkButton(master=self.info_frame, text="Next", command=self.master.destroy)
        self.finish_button.grid(row=1, column=0, padx=20, pady=20, sticky='nesw')
    
    def open_camera(self):
        self.cap = cv2.VideoCapture(0)
        # Declare the width and height in variables 
        width, height = 800, 600
        
        # Set the width and height 
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 
        
        self.decode_barcodes() 
        
    # Function to decode barcodes using brightness normalization
    def decode_barcodes(self):
        
        _, frame = self.cap.read()
         
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

        # Capture the current frame
        _, frame = self.cap.read()

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
        self.camera.photo_image = photo_image 
        self.camera.configure(image=photo_image)
        self.camera.after(10, self.decode_barcodes)


     


# # Create the Tkinter GUI
# root = tk.Tk()
# root.title('Barcode Scanner')

# # Create a label to display the video stream
# label_widget = tk.Label(root)
# label_widget.pack()

# # Start the video capture loop
# while True:
#     process_frame()
#     root.mainloop()
