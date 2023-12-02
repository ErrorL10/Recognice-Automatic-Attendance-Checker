import csv
from datetime import date
import cv2
import face_recognition
from pyzbar.pyzbar import decode
import os
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from Anti_Spoofing.test import test
import customtkinter as ctk
from data_controller import data_controller

path = 'student_images'
name_list = []
files = os.listdir(path)
process = 0


class face_panel(tk.Toplevel):
    def __init__(self):
        super().__init__()
        
        self.title('Face Recognition')
        self.geometry('900x600')
        
        self.camera_frame = camera_frame(master=self)
        self.camera_frame.pack() 
        
        self.controller = data_controller()
        self.controller.fill_attendance()

       
class camera_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.classNames = []
        self.images = []
        self.device_id = 0
        self.isOpened = False
        
        self.camera_panel = ctk.CTkFrame(master=self)
        self.camera_panel.grid(row=0, column=0, sticky='nesw')
        
        self.camera = ctk.CTkLabel(master=self.camera_panel, text="")
        self.camera.grid(row=0, column=0, padx=20, pady=20, sticky='nesw')
        # self.cap  = cv2.VideoCapture(self.device_id)
        self.open_camera_button = ctk.CTkButton(master=self.camera_panel, text="Open Camera", command=self.open_camera)
        self.open_camera_button.grid(row=1, column=0, padx=20, pady=20, sticky='nesw')
        
        self.info_frame = ctk.CTkFrame(master=self)
        self.info_frame.grid(row=0, column=1, sticky='nesw')
        
        #Present Students List
        self.students_list = tk.Listbox(master=self.info_frame)
        self.students_list.grid(row=0, column=0, padx=20, pady=20, sticky='nesw')
        
        #Next Button5
        self.next_button = ctk.CTkButton(master=self.info_frame, text="Next", command=self.start_barcode_attendance)
        self.next_button.grid(row=1, column=0, padx=20, pady=20, sticky='nesw')
    
    def open_camera(self):
        for file in files:
            self.curImg = cv2.imread(f'{path}/{file}')
            self.images.append(self.curImg)
            self.classNames.append(os.path.splitext(file)[0])

        self.encoded_face_train = self.findEncodings()
        
        self.cap = cv2.VideoCapture(self.device_id)
        self.detect_face()
        self.isOpened = True
        
        
    def start_barcode_attendance(self):
        from barcode_window import barcode_window
        if self.isOpened:
            self.cap.release()
            self.isOpened = False
            
        self.master.destroy()
        barcode = barcode_window()
        barcode.mainloop  
    
    def findEncodings(self):
            self.encodeList = []
            for img in self.images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                try:
                    encoded_face = face_recognition.face_encodings(img)[0]
                except IndexError as e:
                    print("No Faces Detected")
                    
                self.encodeList.append(encoded_face)
            return self.encodeList

    def markAttendance(self, name):
        controller = data_controller()
        students = controller.get_students()
        
        name = name.title()
        if name not in name_list: 
            name_list.append(name)
            
            student_number = 0
            for student in students:
                if student[1] == name:
                    student_number = student[0]
            
            today = date.today()
            date_today = today.strftime("%Y/%m/%d")
            
            import time
            time_today = time.strftime("%H:%M:%S")
            
            student_info = f"{student_number}\n{name}"
            self.students_list.insert(0, student_info)
            controller.write_face_attendance(self.update_attendance(student_number))

    def update_attendance(self, student_number):
        import time
        time_today = time.strftime("%H:%M:%S")
            
        updated_value = []
        with open('attendance.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == str(student_number):
                    row[3] = 1
                    row[4] = time_today
                updated_value.append(row)
        
        return updated_value
    
    def detect_face(self):
        try:
            success, self.img = self.cap.read()
            imgS = cv2.resize(self.img, (0,0), None, 0.25,0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            faces_in_frame = face_recognition.face_locations(imgS)
            self.encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
        
            for encode_face, faceloc in zip(self.encoded_faces,faces_in_frame):
                matches = face_recognition.compare_faces(self.encoded_face_train, encode_face, tolerance=0.9)
                faceDist = face_recognition.face_distance(self.encoded_face_train, encode_face)
                matchIndex = np.argmin(faceDist)
                print(matchIndex)
                
                isFake = test(image=imgS, model_dir="Anti_Spoofing/resources/anti_spoof_models", device_id= self.device_id)
            
                if matches[matchIndex] and isFake == 1:
                    name = self.classNames[matchIndex].upper().lower()
                    y1,x2,y2,x1 = faceloc
                    # since we scaled down by 4 times
                    y1, x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(self.img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(self.img, (x1,y2-35),(x2,y2), (0,255,0), cv2.FILLED)
                    cv2.putText(self.img,name, (x1+6,y2-5), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    self.markAttendance(name)
                else:
                    print("Fake")
                    
            self.video_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            # Convert the processed frame to PIL Image format
            processed_image = Image.fromarray(self.video_img)

            # Convert the PIL Image to Tkinter PhotoImage67
            video_label = ImageTk.PhotoImage(image=processed_image)
            
            self.camera.photo_image = video_label
            self.camera.configure(image=video_label)
            self.camera.after(10, self.detect_face)
        except cv2.error as e:
            s = str(e)
            print(s)
        except Exception as e:
            s = str(e)
            print(s)
            




