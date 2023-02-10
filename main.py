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
)
from qrcode_reader import read_qr


def database_ops():

    st.markdown("# View Database")
    view_db = st.button("View Database")
    if view_db:
        show_db()
    st.markdown("""---""")

    st.markdown("# Run Query")
    query = st.text_area("SQL Query", height=100)
    submitted = st.button("Run Query")
    if submitted:
        execute_query(query)
    st.markdown("""---""")

    st.markdown("# Reset Database")
    reset_db = st.button("Reset Database")
    if reset_db:
        reinitialize_db()
    st.markdown("""---""")

    st.markdown(" # Upload Data")
    upload_data()
    st.markdown("""---""")


def generate_invite():
    booking_name = st.text_input("Enter the name of the person you want to invite")
    booking_mobile = st.text_input(
        "Enter the mobile number of the person you want to invite"
    )
    seats_total = st.text_input("Enter the number of seats you want to book")

    generate = st.button("Generate Invite")
    if all(
        [
            generate,
            booking_name,
            booking_mobile,
            seats_total,
        ]
    ):
        insert_row_into_db(booking_name, booking_mobile, seats_total)
        byte_im = generate_invite_graphic(st.session_state.uuid_tmp)
        st.write("Invite generated successfully!")
        st.write("Your unique invite code is: ", st.session_state.uuid_tmp)
        btn = st.download_button(
            label="Download Invite",
            data=byte_im,
            file_name=f"Invitation_{booking_name}.jpg",
            mime="image/jpeg",
        )
        st.markdown("""---""")
        st.image(byte_im)


def manage_entry():
    image = st.camera_input("Scan QR code")
    if image is not None:
        data, qr = read_qr(image)
        print(data)
        if data:
            st.write("Data read successfully!")
            st.write(f"Data: <{data}>")
            st.image(qr)
        else:
            st.write(f"No data found in QR code")


page_names_to_funcs = {
    # "Upload Data": upload_data,
    # "Run Query": run_query,
    "Generate Invite": generate_invite,
    "Manage Entry": manage_entry,
    "Database Ops": database_ops,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
