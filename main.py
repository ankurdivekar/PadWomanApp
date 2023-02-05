import streamlit as st
import cv2
import numpy as np

tabs = st.tabs(["Door Entry Manager", "Invite Generator"])

tab_invite = tabs[1]
with tab_invite:
    st.text("Enter the name of the person you want to invite")
    name = st.text_input("Name")
    st.button("Generate Invite")
    if name:
        st.text(f"Generating invite for {name}")

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
