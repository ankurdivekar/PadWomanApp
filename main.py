import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner

# tabs = st.tabs(["Invite Generator", "Door Entry Manager"])

# tab_invite = tabs[0]
# with tab_invite:
#     st.text("Invite Generator")
#     st.text("Enter the name of the person you want to invite")
#     name = st.text_input("Name")
#     st.button("Generate Invite")

#     if name:
#         st.text(f"Generating invite for {name}")

# tab_door = tabs[1]
# with tab_door:
# qr_code = None
# st.text("Door Entry Manager")
# st.text("Scan the QR code to provide entry")

# if st.button("Scan QR Code"):
#     qr_code = qrcode_scanner(key="qrcode_scanner")

# if qr_code:
#     st.write(qr_code)

qr_code = qrcode_scanner(key="qrcode_scanner")

if qr_code:
    st.write(f"QR content: {qr_code}")
