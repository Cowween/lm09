import cv2

cap = cv2.VideoCapture('rtsp://Cowwin:123456@192.168.31.146/stream2')

while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
