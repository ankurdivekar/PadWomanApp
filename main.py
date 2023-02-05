import streamlit as st
import cv2
from PIL import Image
import numpy as np
import qrcode
from pathlib import Path
from io import BytesIO

tabs = st.tabs(["Door Entry Manager", "Invite Generator"])

tab_door = tabs[0]
with tab_door:
    image = st.camera_input("Scan QR code")

if image is not None:
    bytes_data = image.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()

    data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

    st.write("Here!")
    st.write(data)
    st.image(cv2_img)

tab_invite = tabs[1]
with tab_invite:

    booking_name = st.text_input("Enter the name of the person you want to invite")
    booking_mobile = st.text_input(
        "Enter the mobile number of the person you want to invite"
    )
    seats_total = st.text_input("Enter the number of seats you want to book")

    st.button("Generate Invite")
    if booking_name and booking_mobile and seats_total:

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

        st.text(f"Invite for {seats_total} seats generated for {booking_name}")

        btn = st.download_button(
            label="Download Invite",
            data=byte_im,
            file_name="YourInvitation.jpg",
            mime="image/jpeg",
        )
