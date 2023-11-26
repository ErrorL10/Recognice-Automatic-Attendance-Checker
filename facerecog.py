import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
from Anti_Spoofing.test import test

path = 'student_images'

images = []
classNames = []
name_list = []
files = os.listdir(path)

for file in files:
    curImg = cv2.imread(f'{path}/{file}')
    images.append(curImg)
    classNames.append(os.path.splitext(file)[0])
    
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encoded_face = face_recognition.face_encodings(img)[0]
        except IndexError as e:
            print("No Faces Detected")
            
        encodeList.append(encoded_face)
    return encodeList

encoded_face_train = findEncodings(images)


def markAttendance(name):
    
    if name not in name_list: 
        name_list.append(name)
        students_list.insert(0, name.capitalize())
    # with open('Attendance.csv','r+') as f:
    #     myDataList = f.readlines()
    #     name_list = []
    #     for line in myDataList:
    #         entry = line.split(',')
    #         nameList.append(entry[0])
    #     if name not in nameList:
    #         now = datetime.now()
    #         time = now.strftime('%I:%M:%S:%p')
    #         date = now.strftime('%d-%B-%Y')
    #         f.writelines(f'\n{name}, {time}, {date}')

device_id = 0
cap  = cv2.VideoCapture(device_id)

def detect_face():
    try:
        success, img = cap.read()
        imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faces_in_frame = face_recognition.face_locations(imgS)
        encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
    except cv2.error() as e:
        print("Skill Issue: ", e)
        
    
    for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
        matches = face_recognition.compare_faces(encoded_face_train, encode_face, tolerance=0.9)
        faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
        matchIndex = np.argmin(faceDist)
        print(matchIndex)
        
        isFake = test(image=imgS, model_dir="Anti_Spoofing/resources/anti_spoof_models", device_id= device_id)
        print(isFake)
    
        if matches[matchIndex] and isFake == 1:
            name = classNames[matchIndex].upper().lower()
            y1,x2,y2,x1 = faceloc
            # since we scaled down by 4 times
            y1, x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img, (x1,y2-35),(x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img,name, (x1+6,y2-5), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
        else:
            print("Fake ass")
            
    video_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Convert the processed frame to PIL Image format
    processed_image = Image.fromarray(video_img)

    # Convert the PIL Image to Tkinter PhotoImage67
    video_label = ImageTk.PhotoImage(image=processed_image)
        
    label_widget.photo_image = video_label
    label_widget.configure(image=video_label)
    label_widget.after(10, detect_face)

    
#GUI
root = tk.Tk()
root.title('Barcode Scanner')

# Camera display
label_widget = tk.Label(root)
label_widget.pack()

#Present Students List
students_list = tk.Listbox(root)
students_list.pack()
    
while True:
    detect_face()
    root.mainloop()

    if not tk.Toplevel.winfo_exists(root):
        cap.release()
        cv2.destroyAllWindows()
        break


