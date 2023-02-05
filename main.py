import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
from streamlit_toggle import st_toggle_switch


# # tabs = st.tabs(["Invite Generator", "Door Entry Manager"])

# # tab_invite = tabs[0]
# # with tab_invite:
# #     st.text("Invite Generator")
# #     st.text("Enter the name of the person you want to invite")
# #     name = st.text_input("Name")
# #     st.button("Generate Invite")

# #     if name:
# #         st.text(f"Generating invite for {name}")

# # tab_door = tabs[1]
# # with tab_door:
# # qr_code = None
# # st.text("Door Entry Manager")
# # st.text("Scan the QR code to provide entry")

# # if st.button("Scan QR Code"):
# #     qr_code = qrcode_scanner(key="qrcode_scanner")

# # if qr_code:
# #     st.write(qr_code)


def clear_form():
    st.session_state["foo"] = "clear"
    st.session_state["bar"] = ""
    # st.session_state["qr_toggle"] = False

    print(st.session_state)
    print("~" * 20)


def display_data(qr_string):
    st.write(f"QR content: {qr_string}")

    st.session_state["BookingName"] = info[0]
    st.session_state["BookingNumber"] = info[1]
    st.session_state["SeatsTotal"] = info[2]
    st.session_state["SeatsOccupied"] = info[3]
    st.session_state["SeatsAvailable"] = info[4]


toggle = st_toggle_switch(
    label="Scan",
    key="qr_toggle",
    default_value=False,
    label_after=True,
    # inactive_color="#D3D3D3",
    active_color="#ff567f",
    # track_color="#29B5E8",
)

# with st.form("myform"):
#     f1, f2, f5 = st.columns([1, 1, 1])
#     with f1:
#         st.text_input("Foo", key="foo", disabled=not toggle)
#     with f2:
#         st.text_input("Bar", key="bar")
#     with f5:
#         toggle

#     f3, f4 = st.columns([1, 1])
#     with f3:
#         submit = st.form_submit_button(label="Submit")
#     with f4:
#         clear = st.form_submit_button(label="Clear", on_click=clear_form)

# if submit:
#     st.write("Submitted")

# if clear:
#     st.write("Cleared")
qr_data = None

if toggle and not qr_data:
    qr_data = qrcode_scanner(key="qrcode_scanner")


if qr_data:
    info = qr_data.split(", ")
    print(f"{info = }")
    if len(info) != 5:
        st.write("Invalid QR Code")
        st.stop()
    else:
        st.write(f"Booking Name: {info[0]}")
        st.write(f"Booking Number: {info[1]}")
        st.write(
            f"Seats Total: {info[2]}, Seats Occupied: {info[3]}, Seats Available: {info[4]}"
        )
        if int(info[4]) > 0:
            entry = st.selectbox("Register entry", list(range(1, int(info[4]) + 1)))
            st.button("Confirm")
            print(entry)
        else:
            st.write("No more seats available!")

# # qr_info = None

# if "qr_toggle" not in st.session_state:
#     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#     st.session_state.qr_toggle = False
# st.text(f"{st.session_state.qr_toggle = }")

# # if "qr_info" not in st.session_state:
# #     st.session_state.qr_info = None
# # st.text(f"{st.session_state.qr_info = }")

# if "qrcode_scanner" not in st.session_state:
#     st.session_state.qrcode_scanner = None
# st.text(f"{st.session_state.qrcode_scanner = }")

# # st.text(f"{qr_info = }")


# # qr_code = None
# # if st.session_state.qr_toggle or qr_toggle():

# #     # if st.button("Scan QR Code"):
# #     #     st.session_state.qr_toggle = False

# #     qr_info = qrcode_scanner(key="qrcode_scanner")

# #     if qr_info:
# #         st.session_state.qr_info = qr_info

# # st.write(f"QR content: {st.session_state.qr_info}")
# qr = qr_toggle()

# if st.session_state.qr_toggle or qr:
#     qrcode_scanner(key="qrcode_scanner")

#     if st.session_state.qrcode_scanner:
#         print(f"Scanned QR Code: {st.session_state.qrcode_scanner}")
#         st.session_state.qrcode_scanner = None
#     # st.session_state.qr_info = qr_info
#     # st.session_state.qr_toggle = False
#     # print(qr_info)
#     # st.write(f"QR content: {st.session_state.qrcode_scanner = }")

# print("~~~~~~~~~~~~~~~~~~~~~")
# print(st.session_state)

# # st.session_state.qr_toggle = False
# # print(qr_info)
# # else:
# #     st.session_state.qr_info = None

# # qr_code = qrcode_scanner(key="qrcode_scanner")

# # if qr_info:
# #     st.write(f"QR content: {qr_info}")
