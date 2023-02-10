import cv2
import numpy as np


def read_qr(image):
    detector = cv2.QRCodeDetector()

    bytes_data = image.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

    if data:
        return data, straight_qrcode
    else:
        # Invert image
        cv2_img = cv2.bitwise_not(cv2_img)
        data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

    return data, straight_qrcode
