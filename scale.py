import serial
import mysql.connector as sql
from datetime import datetime
import time

mydb = sql.connect(
    host="localhost",
    user="root",
    password='',
    database='bird_data'
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
while True:

    rfid = rfid_ser.read(11)
    if rfid:
        scale_ser.write(bytes('Q\r\n', 'ascii'))
        time.sleep(1)
        while scale_ser.inWaiting() > 0:
            weight = scale_ser.readline()
            weight_int = ''.join([x for x in weight if (x.isdigit() or x == '.')])
            # weight = bytes_to_long(weight)
            insert_bird_query = f'INSERT INTO birds (rfid, time, date, weight) VALUES ("{str(rfid)[2:12]}", "{datetime.now().strftime("%H:%M:%S")}", "{datetime.now().strftime("%d/%m/%y")}", "{int(weight_int)}")'
            print(insert_bird_query)
            cursor.execute(insert_bird_query)
            mydb.commit()
            rfid = None