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

    # print(f"\n\n{data=}\n\n{bbox=}\n\n{straight_qrcode=}\n\n")
    # if bbox is not None:
    #     # Draw bounding box on qr code in image
    #     straight_qrcode = cv2.rectangle(
    #         cv2_img, tuple(bbox[0]), tuple(bbox[2]), (255, 0, 0), 2
    #     )

    return data, straight_qrcode
