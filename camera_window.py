import tkinter as tk
import customtkinter as ctk
import cv2
from data_controller import data_controller
from PIL import Image, ImageTk

class camera_window(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        self.title('Add Pictures')
        self.i = 0

        self.canvas = tk.Canvas(self, width=640, height=480)
        self.canvas.pack()

        self.btn_snapshot = ctk.CTkButton(master=self, text="Take Picture", command=self.take_picture)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        self.video = cv2.VideoCapture(0)
        self.delay = 15
        self.update()

    def take_picture(self):
        if self.i <= 4:
            ret, frame = self.video.read()
            if ret:
                cv2.imwrite("student_images/temp/image{}.jpg".format(self.i), frame)
                self.i += 1
        else:
            self.video.release()
            self.destroy()

    def update(self):
        ret, frame = self.video.read()
        if ret:
            self.pic = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.pic))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.after(self.delay, self.update)

