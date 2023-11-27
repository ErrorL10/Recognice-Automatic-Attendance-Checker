import cv2
import face_recognition
from pyzbar.pyzbar import decode
import os
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from Anti_Spoofing.test import test
import customtkinter as ctk

path = 'student_images'

name_list = []
files = os.listdir(path)

class face_panel(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title('Face Recognition')
        self.geometry('900x600')
        
        self.camera_frame = camera_frame(master=self)
        self.camera_frame.pack() 

       
class camera_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.classNames = []
        self.images = []
        self.process = 0
        
        self.label_widget = ctk.CTkLabel(master=self)
        
        for file in files:
            self.curImg = cv2.imread(f'{path}/{file}')
            self.images.append(self.curImg)
            self.classNames.append(os.path.splitext(file)[0])

        self.encoded_face_train = self.findEncodings()

        self.device_id = 0
        self.cap  = cv2.VideoCapture(self.device_id)
        
        if self.process == 0:
            self.detect_face()
        else:
            self.label_widget.after_cancel(self.label_widget.after_id)
            self.decode_barcodes()
        
        self.label_widget.grid(row=0, column=0, padx=20, pady=20, sticky='nesw')
        
        self.info_frame = ctk.CTkFrame(master=self)
        self.info_frame.grid(row=0, column=1, padx=20, pady=20, sticky='nesw')
        
        #Present Students List
        self.students_list = tk.Listbox(master=self.info_frame)
        self.students_list.grid(row=0, column=0, padx=20, pady=20, sticky='nesw')
        
        #Next Button5
        self.next_button = ctk.CTkButton(master=self.info_frame, text="Next", command=self.start_barcode_attendance)
        self.next_button.grid(row=1, column=0, padx=20, pady=20, sticky='nesw')
    
    def start_barcode_attendance(self):
        self.process = 1
        print(self.process)

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
        
        if name not in name_list: 
            name_list.append(name)
            self.students_list.insert(0, name.capitalize())
    

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
            
            self.label_widget.photo_image = video_label
            self.label_widget.configure(image=video_label)
            self.label_widget.after(10, self.detect_face)
        except:
            print("Skill Issue: ")
            
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

        # Draw bounding boxes
        for obj in decoded_objects:
            x, y, w, h = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, str(obj.data), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
        processed_image = Image.fromarray(frame)

        photo_image = ImageTk.PhotoImage(image=processed_image)

        # Update the video label with the new frame
        self.label_widget.photo_image = photo_image 
        self.label_widget.configure(image=photo_image)
        self.label_widget.after(10, self.decode_barcodes)

               
if __name__ == "__main__":
    face = face_panel()
    face.mainloop()






