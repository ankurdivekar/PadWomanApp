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

    st.text("Enter the name of the person you want to invite")
    name = st.text_input("Name")
    st.button("Generate Invite")
    if name:
        st.text(f"Generating invite for {Path(__file__).parent}")

        # Generate invite here

        logo = Image.open(Path(__file__).parent / "Assets/Logo.jpg")
        # taking base width
        basewidth = 100

        # adjust image size
        wpercent = basewidth / float(logo.size[0])
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

        BookingName = "Ankur Divekar"
        BookingMobile = "9923317669"
        SeatsTotal = "12"

        QRcode.add_data(f"{BookingName}, {BookingMobile}, {SeatsTotal}")
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
        invite = Image.open(Path(__file__).parent / "Assets/InviteTemplate.bmp")

        invite.paste(QRimg2, (730, 40))

        # invite.save(Path(__file__).parent / "Assets/YourInvite.png")

        print("Invite generated!")

        buf = BytesIO()
        invite.save(buf, format="JPEG")
        byte_im = buf.getvalue()

        btn = st.download_button(
            label="Download Image",
            data=byte_im,
            file_name="YourInvitation.jpg",
            mime="image/jpeg",
        )
