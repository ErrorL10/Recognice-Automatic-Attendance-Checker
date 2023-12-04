import csv
from tkinter import messagebox
import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import tkinter as tk
import customtkinter as ctk
from data_controller import data_controller

student_number_list = []

class barcode_window(ctk.CTkToplevel):
    def __init__(self, section):
        super().__init__()
        
        self.section = section
        self.title('Barcode Scanner')
        
         # Color Theme 
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.main_label = ctk.CTkLabel(master=self.main_frame, text="Barcode Attendance", font=("Roboto", 24))
        self.main_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.camera_frame = camera_frame(master=self.main_frame, section=self.section)
        self.camera_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

class camera_frame(ctk.CTkFrame):
    def __init__(self, master, section, **kwargs):
        super().__init__(master, **kwargs)
        
        self.controller = data_controller()
        self.section = section
        self.camera_panel = ctk.CTkFrame(master=self)
        self.camera_panel.grid(row=0, column=0, sticky='nesw')
        
        self.camera = ctk.CTkLabel(master=self.camera_panel, height=400, width=600, text="")
        self.camera.grid(row=0, column=0, padx=20, pady=20, sticky='nesw')
        
        self.open_camera_button = ctk.CTkButton(master=self.camera_panel, text="Open Camera", command=self.open_camera)
        self.open_camera_button.grid(row=1, column=0, padx=20, pady=20, sticky='nesw')
        
        self.info_frame = ctk.CTkFrame(master=self)
        self.info_frame.grid(row=0, column=1, sticky='nesw')
        
        #Present Students List
        self.students_list = tk.Listbox(master=self.info_frame)
        self.students_list.grid(row=0, column=0, padx=20, pady=20, sticky='nesw')
        
        #Next Button
        self.finish_button = ctk.CTkButton(master=self.info_frame, text="Finish", command=self.end_attendance)
        self.finish_button.grid(row=1, column=0, padx=20, pady=20, sticky='nesw')
    
    def open_camera(self):
        self.cap = cv2.VideoCapture(1)
        self.decode_barcodes() 
    
    def end_attendance(self):
        confirm = messagebox.askyesno("Warning", "Do you wish to end checking the attendance? This action is irreversible", parent=self)
        if confirm:
            root = self.winfo_toplevel()
            root.destroy()
            self.controller.insert_attendance()
        else:
            print("Attendance continue")
    
    # Function to decode barcodes using brightness normalization
    def decode_barcodes(self):
        students = self.controller.get_students(self.section)
        
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
            barcode_data = obj.data.decode('utf-8')
 
            recognized = False
            barcode_int = int(barcode_data) if barcode_data.isdigit() else "No"
            for student in students:
                if student[0] == barcode_int:
                    recognized = True
                    
                    
            if recognized:
                x, y, w, h = obj.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                self.mark_attendance(barcode_int)
            else:
                x, y, w, h = obj.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Not Recognized", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
        # Convert the processed frame to PIL Image format
        processed_image = Image.fromarray(frame)

        # Convert the PIL Image to Tkinter PhotoImage67
        photo_image = ImageTk.PhotoImage(image=processed_image)

        # Update the video label with the new frame
        self.camera.photo_image = photo_image 
        self.camera.configure(image=photo_image)
        self.camera.after(10, self.decode_barcodes)

    def mark_attendance(self, student_number):
        controller = data_controller()
        students = controller.get_students(self.section)
        
        if student_number not in student_number_list: 
            student_number_list.append(student_number)
            
            student_name = ""
            for student in students:
                if student[0] == student_number:
                    student_name = student[1]
            
            updated_value = self.update_attendance(student_number)
            
            self.students_list.insert(0, student_name)
            controller.write_barcode_attendance(updated_value)
     
    def update_attendance(self, student_number):
        import time
        time_today = time.strftime("%H:%M:%S")
            
        updated_value = []
        with open('attendance.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == str(student_number):
                    row[6] = 1
                    row[7] = time_today

                    print(row[4], row[6])
                    if int(row[4]) == 1 and int(row[6]) == 1:
                        row[8] = 'Present'
                        print(row[8])  
                    else:
                        row[8] = 'Absent'
                        print(row[8])
                    
                updated_value.append(row)
        
        return updated_value
    
    


