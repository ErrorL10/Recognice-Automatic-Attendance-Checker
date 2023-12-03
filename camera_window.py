import tkinter as tk
import customtkinter as ctk
import cv2
from data_controller import data_controller
from PIL import Image, ImageTk

class camera_window(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title('Add Pictures')
            
        # Color Theme 
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.camera_label = ctk.CTkLabel(master=self, text="Add Pictures", font=("Roboto", 32))
        self.camera_label.grid(row=0, column=0, sticky='nesw')
        
        self.camera_panel = ctk.CTkFrame(master=self)
        self.camera_panel.grid(row=1, column=0, sticky='nesw')
    
        self.camera = tk.Label(master=self.camera_panel, height=400, width=600, text="")
        self.camera.grid(row=0, column=0, padx=20, pady=20, sticky='ew')
        self.open_camera()
        
    def open_camera(self):
        self.cap = cv2.VideoCapture(0)
        
        success, self.img = self.cap.read()
        self.video_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        # Convert the processed frame to PIL Image format
        processed_image = Image.fromarray(self.video_img)

         # Convert the PIL Image to Tkinter PhotoImage67
        video_label = ImageTk.PhotoImage(image=processed_image)
            
        self.camera.photo_image = video_label
        self.camera.configure(image=video_label)
        self.camera.after(10, self.open_camera)