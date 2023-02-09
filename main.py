import sqlite3
import streamlit as st
import pandas as pd
import os
import uuid


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        st.write(e)

    return conn


def database_ops():

    db_file = st.secrets["db_file"]
    table_name = st.secrets["table_name"]

    st.markdown("# View Database")
    view_db = st.button("View Database")
    if view_db:

        with create_connection(db_file) as conn:
            st.write(conn)  # success message?

            query = conn.execute("SELECT * FROM Registrations")
            cols = [column[0] for column in query.description]
            results_df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
            st.dataframe(results_df)

    st.markdown("# Run Query")

    query = st.text_area("SQL Query", height=100)
    conn = create_connection(db_file)

    submitted = st.button("Run Query")

    if submitted:
        try:
            # cur = conn.cursor()
            # cur.execute(query)
            # conn.commit()

            query = conn.execute(query)
            cols = [column[0] for column in query.description]
            results_df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
            st.dataframe(results_df)
        except Exception as e:
            st.write(e)

    st.markdown("# Reset Database")
    reset_db = st.button("Reset Database")
    if reset_db:

        with create_connection(db_file) as conn:
            st.write(conn)  # success message?
            cur = conn.cursor()
            cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            cur.execute(
                f"CREATE TABLE {table_name} (UUID UID, BookingName TEXT, BookingPhone TEXT PRIMARY KEY, SeatsTotal INTEGER, SeatsOccupied INTEGER)"
            )
            cur.execute(
                "INSERT INTO Registrations (UUID, BookingName, BookingPhone, SeatsTotal, SeatsOccupied) VALUES (?, ?, ?, ?, ?)",
                (str(uuid.uuid1()), "Ankur", "12345", 12, 0),
            )
            conn.commit()
    st.sidebar.markdown("# Run Query")


# def upload_data():
#     st.markdown("# Upload Data")
#     # https://discuss.streamlit.io/t/uploading-csv-and-excel-files/10866/2
#     sqlite_dbs = [file for file in os.listdir(".") if file.endswith(".db")]
#     db_filename = st.selectbox("DB Filename", sqlite_dbs)
#     table_name = st.text_input("Table Name to Insert")
#     conn = create_connection(db_filename)
#     uploaded_file = st.file_uploader("Choose a file")
#     if uploaded_file is not None:
#         # read csv
#         try:
#             df = pd.read_csv(uploaded_file)
#             df.to_sql(name=table_name, con=conn)
#             st.write("Data uploaded successfully. These are the first 5 rows.")
#             st.dataframe(df.head(5))

#         except Exception as e:
#             st.write(e)


# def run_query():
#     st.markdown("# Run Query")
#     sqlite_dbs = [file for file in os.listdir(".") if file.endswith(".db")]
#     db_filename = st.selectbox("DB Filename", sqlite_dbs)

#     query = st.text_area("SQL Query", height=100)
#     conn = create_connection()

#     submitted = st.button("Run Query")

#     if submitted:
#         try:
#             # cur = conn.cursor()
#             # cur.execute(query)
#             # conn.commit()

#             query = conn.execute(query)
#             cols = [column[0] for column in query.description]
#             results_df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
#             st.dataframe(results_df)
#         except Exception as e:
#             st.write(e)

#     st.sidebar.markdown("# Run Query")


def insert_row_into_db(bname, bmobile, seats_total):
    uuid_tmp = str(uuid.uuid1())
    with create_connection(st.secrets["db_file"]) as conn:
        cur = conn.cursor()

        cur.execute(
            "INSERT OR IGNORE INTO Registrations (UUID, BookingName, BookingPhone, SeatsTotal, SeatsOccupied) VALUES (?, ?, ?, ?, ?)",
            (uuid_tmp, bname, bmobile, 0, 0),
        )
        cur.execute(
            "UPDATE Registrations SET SeatsTotal = SeatsTotal + ? WHERE BookingPhone = ?",
            (seats_total, bmobile),
        )

        # cur.execute(
        #     "INSERT INTO Registrations (UUID, BookingName, BookingPhone, SeatsTotal, SeatsOccupied) VALUES (?, ?, ?, ?, ?)",
        #     (uuid_tmp, bname, bmobile, seats_total, "0"),
        # )
        conn.commit()
    st.session_state.uuid_tmp = uuid_tmp


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
        st.write("Invite generated successfully!")
        st.write("Your unique invite code is: ", st.session_state.uuid_tmp)


page_names_to_funcs = {
    # "Upload Data": upload_data,
    # "Run Query": run_query,
    "Generate Invite": generate_invite,
    "Database Ops": database_ops,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
