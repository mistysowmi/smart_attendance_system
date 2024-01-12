import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime
import pyttsx3


video_capture = cv2.VideoCapture(0)
r_img = face_recognition.load_image_file("static/rathi.jpg")
rathi_encoding = face_recognition.face_encodings(r_img)[0]
s_img = face_recognition.load_image_file("static/sowmi.jpg")
sowmi_encoding = face_recognition.face_encodings(s_img)[0]
d_img = face_recognition.load_image_file("static/dharshini.jpg")
dharshini_encoding = face_recognition.face_encodings(d_img)[0]
speak = pyttsx3.init()

known_encoding = [rathi_encoding,sowmi_encoding,dharshini_encoding]

known_names = [ "rathi","sowmi","dharshini"]


students = known_names.copy()

face_locations = []
new_encodings = []



now = datetime.now()
date = now.strftime("%Y-%m-%d")


f = open(date+'.csv','w+',newline = '')
write = csv.writer(f)


while True:
    _,frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_frame = small_frame[:,:,::-1]
    
    if True:
        face_locations = face_recognition.face_locations(rgb_frame)
        new_encodings = face_recognition.face_encodings(rgb_frame,face_locations)
        for face_encoding in new_encodings:
            match = face_recognition.compare_faces(known_encoding,face_encoding)
            name=""
            face_distance = face_recognition.face_distance(known_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            if match[best_match_index]:
                name = known_names[best_match_index]
            
            
           
            if name in known_names:
                if name in students:
                    students.remove(name)
                    print(students)
                    time = now.strftime("%H-%M-%S")
                    write.writerow([name,time])
                    note ="welcome"+name
                    speak.say(note)
                    speak.runAndWait()
            
    cv2.imshow("attendence system",frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
        
video_capture.release()
cv2.destroyAllWindows()
f.close()


