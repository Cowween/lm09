import serial
import mysql.connector as sql
from datetime import datetime
import calculation
import time
import cv2
import os
from PIL import Image
from model_test import prediction


def camera_capture(pic):
    cv2.imwrite(os.path.join("dump/images", "feeder.jpg"), pic)
    image = Image.open('dump/images/feeder.jpg')

    correct_size = image.resize((224, 224))
    correct_size.save('dump/images/feeder.jpg')

    print(prediction("dump"))


cap = cv2.VideoCapture('rtsp://Cowwin:12345678@192.168.1.100/stream2')
mydb = sql.connect(
    host="localhost",
    user="root",
    password='',
    database='birds'
)
cursor = mydb.cursor()

scale_ser = serial.Serial(
   port='COM4',
   baudrate=2400,
   parity=serial.PARITY_ODD,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.SEVENBITS
)

rfid_ser = serial.Serial(
    port='COM3',
    baudrate=19200,
)

# print("Hello world")
rfid = None
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if rfid_ser.inWaiting() > 0:
        rfid = rfid_ser.read(11)
    if rfid:
        scale_ser.write(bytes('Q\r\n', 'ascii'))
        time.sleep(1)
        camera_capture(frame)
        while scale_ser.inWaiting() > 0:
            weight = scale_ser.readline()
            weight_int = ''.join([x for x in str(weight) if (x.isdigit() or x == '.')])
            # weight = bytes_to_long(weight)
            insert_bird_query = f'INSERT INTO birds (rfid, time, date, weight) VALUES ("{str(rfid)[2:12]}", "{datetime.now().strftime("%H:%M:%S")}", "{datetime.now().strftime("%d/%m/%y")}", "{int(float(weight_int))}")'
            print(insert_bird_query)
            cursor.execute(insert_bird_query)
            mydb.commit()
            mean = calculation.calculate_mean(cursor)
            cursor.execute("select * from birds order by id desc limit 1;")
            if abs((mean - float(weight_int))/mean) >= 0.1:
                print('ERROR!!!')
                message = str(cursor.fetchall())
                message = message.replace(':', ' ')
                print(message)
                #calculation.send_email(message, '191321y@student.hci.edu.sg')
            rfid = None
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()