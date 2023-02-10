import cv2
from PIL import Image
import numpy as np
import qrcode
from pathlib import Path
from io import BytesIO
import streamlit as st


def generate_invite_graphic(booking_uuid):

    # Generate invite
    # logo = Image.open(Path(__file__).parents[0] / "assets/Logo.jpg")
    # basewidth = 295

    # adjust image size
    # wpercent = basewidth / float(logo.size[0])
    # hsize = int((float(logo.size[1]) * float(wpercent)))
    # logo = logo.resize((basewidth, hsize), Image.LANCZOS)
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

    QRcode.add_data(f"PadWoman2:{booking_uuid}")
    QRcode.make(fit=True)

    QRimg = QRcode.make_image(
        fill_color="white",  # (253, 154, 0),
        back_color=(93, 18, 12),
    ).convert("RGB")

    # set size of QR code
    # pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
    # QRimg.paste(logo, pos)

    qr_final_size = 295
    QRimg2 = QRimg.resize((qr_final_size, qr_final_size), Image.LANCZOS)

    # Get invite image
    invite = Image.open(Path(__file__).parents[0] / "assets/InviteTemplate.jpg")

    invite.paste(QRimg2, (560, 1180))

    invite.save(Path(__file__).parent / "assets/YourInvite.png")

    buf = BytesIO()
    invite.save(buf, format="JPEG")
    byte_im = buf.getvalue()

    return byte_im
