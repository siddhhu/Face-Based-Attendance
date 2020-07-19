from flask import Flask,render_template,request
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from datetime import date
import sqlite3
name="siddhu"
app = Flask(__name__)
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method=="POST":
        return render_template('index.html')
    else:
        return "All okkk"
@app.route('/name', methods=['GET', 'POST'])
def name():
    if request.method=="POST":
        name1=request.form['name1']
        name2=request.form['name2']
        import cv2
        import os
        cam = cv2.VideoCapture(0)

        cv2.namedWindow("Face Recogniser")

    

        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("Press Space to capture image", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = name1+".png"
                path='E:\\fACErECOGNITION\\ImagesAttendance'
                cv2.imwrite(os.path.join(path,img_name), frame)
                print("{} written!".format(img_name))
                

        cam.release()

        cv2.destroyAllWindows()
        return render_template('image.html')
    else:
        return 'All is not well'

@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        path = 'ImagesAttendance'
        images = []
        classNames = []
        myList = os.listdir(path)
        print(myList)
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        print(classNames)
        
        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                if not len(encode):
                    print( "can't be encoded")
                    continue
                encodeList.append(encode)
            return encodeList

        def markData(name):
            print("The Attended Person is ",name)
            now = datetime.now()
            dtString = now.strftime('%H:00') 
            today = date.today()
            print("Today's date:", today)
            conn = sqlite3.connect('information.db')
            conn.execute('''CREATE TABLE IF NOT EXISTS Attendance
                            (NAME TEXT  NOT NULL,
                             Time  TEXT NOT NULL ,Date TEXT NOT NULL)''')  
                       
            conn.execute("INSERT or Ignore into Attendance (NAME,Time,Date) values (?,?,?)",(name,dtString,today,))
            conn.commit()  
            cursor = conn.execute("SELECT NAME,Time,Date from Attendance")  
                                                                  
            for line in cursor:
                print("Name Updated :",line[0])
                print("Time Updated :",line[1])
            

        
        def markAttendance(name):
            with open('attendance.csv','r+',errors='ignore') as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    print(myDataList)
                    entry = line.split(',')
                    nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S')
                    f.writelines(f'\n{name},{dtString}')
    


        
        # ### FOR CAPTURING SCREEN RATHER THAN WEBCAM
        # def captureScreen(bbox=(300,300,690+300,530+300)):
        #     capScr = np.array(ImageGrab.grab(bbox))
        #     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
        #     return capScr
        
        encodeListKnown = findEncodings(images)
        print('Encoding Complete')
        
        cap = cv2.VideoCapture(0)
        
        while True:
            success, img = cap.read()
            #img = captureScreen()
            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
        
            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
                #print(faceDis)
                matchIndex = np.argmin(faceDis)
        
                if faceDis[matchIndex]< 0.50:
                    name = classNames[matchIndex].upper()
                    markAttendance(name)
                    markData(name)
                else: name = 'Unknown'
                #print(name)
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            cv2.imshow('Punch your Attendance',img)
            c=cv2.waitKey(1)
            if c == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

        return render_template('first.html')
        
    else:
        return render_template('main.html')
@app.route('/how',methods=["GET","POST"])
def how():
    return render_template('form.html')
@app.route('/data',methods=["GET","POST"])
def data():
    user=request.form['username']
    pass1=request.form['pass']
    if user=="tech" and pass1=="tech@321" :
        if request.method=="POST":
            today=date.today()
            print(today)
            conn = sqlite3.connect('information.db')
            conn.row_factory = sqlite3.Row 
            cur = conn.cursor() 
            print ("Opened database successfully");
            cursor = cur.execute("SELECT DISTINCT NAME,Time, Date from Attendance where Date=?",(today,))
            rows=cur.fetchall()
            print(rows)
            for line in cursor:

               data1=list(line)
            print ("Operation done successfully");
            conn.close()

            return render_template('form2.html',rows=rows)
    else:
        return render_template('form1.html')
            
@app.route('/whole',methods=["GET","POST"])
def whole():
    today=date.today()
    print(today)
    conn = sqlite3.connect('information.db')
    conn.row_factory = sqlite3.Row 
    cur = conn.cursor() 
    print ("Opened database successfully");
    cursor = cur.execute("SELECT DISTINCT NAME,Time, Date from Attendance")
    rows=cur.fetchall()    
    return render_template('form3.html',rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
