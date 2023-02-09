import cv2
from PIL import Image
import numpy as np
import qrcode
from pathlib import Path
from io import BytesIO


def generate_invite(booking_name, booking_mobile, seats_total):

    # Generate invite
    logo = Image.open(Path(__file__).parents[0] / "assets/Logo.jpg")
    basewidth = 100

    # adjust image size
    wpercent = basewidth / float(logo.size[0])
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.LANCZOS)
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

    QRcode.add_data(f"{booking_name}, {booking_mobile}, {seats_total}")
    QRcode.make(fit=True)

    QRimg = QRcode.make_image(
        fill_color=(52, 52, 52),
        back_color=(222, 222, 222),
    ).convert("RGB")

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    QRimg2 = QRimg.resize((300, 300), Image.LANCZOS)

    # Get invite image
    invite = Image.open(Path(__file__).parents[0] / "assets/InviteTemplate.bmp")

    invite.paste(QRimg2, (730, 40))

    # invite.save(Path(__file__).parent / "assets/YourInvite.png")

    buf = BytesIO()
    invite.save(buf, format="JPEG")
    byte_im = buf.getvalue()
