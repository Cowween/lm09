import cv2
import keyboard
import os
from PIL import Image
from model_test import prediction
cap = cv2.VideoCapture('rtsp://Cowwin:123456@192.168.31.146/stream2')

while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if keyboard.is_pressed('c'):
        print("capture")
        cv2.imwrite(os.path.join("dump/images", "feeder.jpg"), frame)
        image = Image.open('dump/images/feeder.jpg')

        correct_size = image.resize((224, 224))
        correct_size.save('dump/images/feeder.jpg')

        print(prediction("dump"))
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
