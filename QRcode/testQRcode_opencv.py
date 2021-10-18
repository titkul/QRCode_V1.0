import cv2
# Name of the QR Code Image file
cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
while True:
    ret, frame = cap.read()
    # frame = frame[150:420,150:520]   
    data, vertices_array, binary_qrcode = detector.detectAndDecode(frame)
    # print(data)
    if vertices_array is not None:
        if data:
            print(data)
            xtd = data.split("|")[1]
            cv2.putText(frame, xtd,  (100,100), cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255), 2)
    # else:
    #     cv2.putText(frame, "Unknown",  (100,100), cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255), 2)
    cv2.imshow("frame", frame)
    if  cv2.waitKey(10) == ord('q'):
        break