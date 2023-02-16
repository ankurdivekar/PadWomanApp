import sqlite3
import streamlit as st
import pandas as pd
import os
import uuid
from graphic_maker import generate_invite_graphic
from db_operations import (
    show_db,
    execute_query,
    reinitialize_db,
    insert_row_into_db,
    upload_data,
    get_seats_available,
    update_seats_occupied,
    get_booking_status,
    download_data,
)
from qrcode_reader import read_qr


def database_ops():

    st.markdown("# Check Booking")
    booking_mobile = st.text_input("Enter the booking phone number")
    if booking_mobile and not (
        len(booking_mobile) == 10 and booking_mobile.isnumeric()
    ):
        st.error("Please enter a valid 10-digit mobile number")
    check = st.button("Check")
    if check:
        if all(
            [
                booking_mobile,
                len(booking_mobile) == 10,
                booking_mobile.isnumeric(),
            ]
        ):
            get_booking_status(booking_mobile)
    st.markdown("""---""")

    st.markdown("# View Database")
    view_db = st.button("View Database")
    if view_db:
        show_db()
    st.markdown("""---""")

    st.markdown(" # Download Data")
    download_data()
    st.markdown("""---""")

    # st.markdown(" # Upload Data")
    # upload_data()
    # st.markdown("""---""")

    # st.markdown("# Run Query")
    # query = st.text_area("SQL Query", height=100)
    # submitted = st.button("Run Query")
    # if submitted:
    #     execute_query(query)
    # st.markdown("""---""")

    # st.markdown("# Reset Database")
    # reset_db = st.button("Reset Database")
    # if reset_db:
    #     reinitialize_db()
    # st.markdown("""---""")


# def generate_and_download_invite(booking_name, booking_mobile, seats_total):

#     generate = st.button("Generate Invite")
#     if generate:
#         if all(
#             [
#                 " " in booking_name,
#                 # booking_mobile,
#                 seats_total.isnumeric(),
#                 len(booking_mobile) == 10,
#                 booking_mobile.isnumeric(),
#             ]
#         ):
#             current_uuid = insert_row_into_db(booking_name, booking_mobile, seats_total)
#             byte_im = generate_invite_graphic(current_uuid)
#             st.write("Invite generated successfully!")
#             # st.write("Your unique invite code is: ", current_uuid)
#             btn = st.download_button(
#                 label="Download Invite",
#                 data=byte_im,
#                 file_name=f"Invitation_{booking_name}.jpg",
#                 mime="image/jpeg",
#             )
#             st.markdown("""---""")
#             st.image(byte_im)
#         else:
#             st.error("Please enter all the details correctly!")


def generate_invite():

    booking_name = st.text_input("Enter the name of the person you want to invite")
    if booking_name and not " " in booking_name:
        st.error("Please enter the full name of the person you want to invite")

    booking_mobile = st.text_input(
        "Enter the mobile number of the person you want to invite"
    )
    if booking_mobile and not (
        len(booking_mobile) == 10 and booking_mobile.isnumeric()
    ):
        st.error("Please enter a valid 10-digit mobile number")

    seats_total = st.text_input("Enter the number of seats you want to book")
    if seats_total and not seats_total.isnumeric():
        st.error("Please enter a valid number of seats")

    # generate_and_download_invite(booking_name, booking_mobile, seats_total)

    generate = st.button("Generate Invite")
    if generate:
        if all(
            [
                " " in booking_name,
                # booking_mobile,
                seats_total.isnumeric(),
                len(booking_mobile) == 10,
                booking_mobile.isnumeric(),
            ]
        ):
            current_uuid = insert_row_into_db(booking_name, booking_mobile, seats_total)
            byte_im = generate_invite_graphic(current_uuid)
            st.write("Invite generated successfully!")
            # st.write("Your unique invite code is: ", current_uuid)

            btn = st.download_button(
                label="Download Invite",
                data=byte_im,
                file_name=f"Invitation_{booking_name}.jpg",
                mime="image/jpeg",
            )
            st.markdown("""---""")
            st.image(byte_im)
        else:
            st.error("Please enter all the details correctly!")


def manage_entry():
    image = st.camera_input("Scan QR code")
    if image is not None:
        data, qr = read_qr(image)
        current_uuid = data.split(":")[1] if "PadWoman2" in data else None

        # TODO: Remove this line after testing
        # current_uuid = "3f75ee14-a94f-11ed-8648-b44023536a4f"

        if not current_uuid:
            st.write(f"No booking data found in QR code")
        else:
            # st.write("Data read successfully!")
            # st.write(f"Data: <{data}>")
            # st.image(qr)

            seats_available, booking_name = get_seats_available(current_uuid)
            if booking_name:
                if seats_available <= 0:
                    st.write(f"No more seats available for {booking_name}!")
                else:
                    st.write(f"Seats available for {booking_name}: {seats_available}")
                    # Populate selectbox with available seats from 1 to seats_available
                    entry = st.selectbox(
                        "CONFIRM ENTRY", list(range(0, seats_available + 1))
                    )
                    if entry:
                        st.error(f"Confirm entry for {entry} seats?")
                        if st.button("Yes"):
                            update_seats_occupied(current_uuid, entry)
                            st.write(f"Entry confirmed for {entry} seats!")
            else:
                st.write("No booking found for this QR code!")


st.sidebar.markdown("""---""")
st.sidebar.title("PadWoman2 Event App")
st.sidebar.markdown("Built with :heart: by [Ankur](https://instagram.com/raagarock)")
st.sidebar.markdown("""---""")


page_names_to_funcs = {
    # "Upload Data": upload_data,
    # "Run Query": run_query,
    "Generate Invite": generate_invite,
    "Manage Entry": manage_entry,
    "Database Ops": database_ops,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
