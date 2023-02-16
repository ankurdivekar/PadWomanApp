import sqlite3
import streamlit as st
import pandas as pd
import uuid
import os


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


def show_db():
    with create_connection(st.secrets["db_file"]) as conn:
        st.write(conn)  # success message?

        query = conn.execute(f"SELECT * FROM {st.secrets['table_name']}")
        cols = [column[0] for column in query.description]
        results_df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
        st.dataframe(results_df)


def execute_query(query):
    with create_connection(st.secrets["db_file"]) as conn:
        try:
            query = conn.execute(query)
            cols = [column[0] for column in query.description]
            results_df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
            st.dataframe(results_df)
        except Exception as e:
            st.write(e)


def get_seats_available(current_uuid):
    with create_connection(st.secrets["db_file"]) as conn:

        query = conn.execute(
            f"SELECT BookingName, SeatsTotal, SeatsOccupied FROM {st.secrets['table_name']} WHERE UUID = '{current_uuid}'"
        ).fetchone()

        # print(f"Seats for {current_uuid}: {query}")
        seats_available = 0 if query is None else query[1] - query[2]
        booking_name = "" if query is None else query[0]
        return seats_available, booking_name


def get_booking_status(booking_phone):
    with create_connection(st.secrets["db_file"]) as conn:

        query = conn.execute(
            f"SELECT * FROM {st.secrets['table_name']} WHERE BookingPhone ='{booking_phone}'"
        )
        data = query.fetchall()
        # print(data)
        if data:
            cols = [column[0] for column in query.description]
            results_df = pd.DataFrame.from_records(data=data, columns=cols)
            st.dataframe(results_df)
        else:
            st.write(f"No booking found for {booking_phone}!")


def update_seats_occupied(current_uuid, seats_occupied):
    with create_connection(st.secrets["db_file"]) as conn:
        cur = conn.cursor()
        cur.execute(
            f"UPDATE {st.secrets['table_name']} SET SeatsOccupied = SeatsOccupied + ? WHERE UUID = ?",
            (seats_occupied, current_uuid),
        )
        conn.commit()


def reinitialize_db():
    with create_connection(st.secrets["db_file"]) as conn:
        st.write(conn)  # success message?
        cur = conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {st.secrets['table_name']}")
        cur.execute(
            f"CREATE TABLE {st.secrets['table_name']} (UUID UNIQUE, BookingName TEXT, BookingPhone TEXT PRIMARY KEY, SeatsTotal INTEGER, SeatsOccupied INTEGER)"
        )

        cur.execute(
            "INSERT INTO Registration (UUID, BookingName, BookingPhone, SeatsTotal, SeatsOccupied) VALUES (?, ?, ?, ?, ?)",
            (str(uuid.uuid1()), "Ankur", "1111111111", 14, 0),
        )
        cur.execute(
            "INSERT INTO Registration (UUID, BookingName, BookingPhone, SeatsTotal, SeatsOccupied) VALUES (?, ?, ?, ?, ?)",
            (str(uuid.uuid1()), "Meghana", "2222222222", 10, 0),
        )
        cur.execute(
            "INSERT INTO Registration (UUID, BookingName, BookingPhone, SeatsTotal, SeatsOccupied) VALUES (?, ?, ?, ?, ?)",
            (str(uuid.uuid1()), "Sanket", "3333333333", 17, 0),
        )
        conn.commit()


def insert_row_into_db(bname, bmobile, seats_total):

    with create_connection(st.secrets["db_file"]) as conn:

        # Search for existing entry
        query = conn.execute(
            f"SELECT UUID FROM {st.secrets['table_name']} WHERE BookingPhone = '{bmobile}'"
        ).fetchone()

        cur = conn.cursor()
        if query is None:
            # Insert new entry if not found
            uuid_tmp = str(uuid.uuid1())
            cur.execute(
                "INSERT INTO Registration (UUID, BookingName, BookingPhone, SeatsTotal, SeatsOccupied) VALUES (?, ?, ?, ?, ?)",
                (uuid_tmp, bname, bmobile, seats_total, 0),
            )
        else:
            # Update existing entry if found
            uuid_tmp = query[0]
            cur.execute(
                "UPDATE Registration SET SeatsTotal = SeatsTotal + ? WHERE BookingPhone = ?",
                (seats_total, bmobile),
            )

        conn.commit()
        # cur = conn.cursor()
        # cur.execute(
        #     "INSERT OR IGNORE INTO Registration (UUID, BookingName, BookingPhone, SeatsTotal, SeatsOccupied) VALUES (?, ?, ?, ?, ?)",
        #     (uuid_tmp, bname, bmobile, 0, 0),
        # )
        # cur.execute(
        #     "UPDATE Registration SET SeatsTotal = SeatsTotal + ? WHERE BookingPhone = ?",
        #     (seats_total, bmobile),
        # )

        # cur.execute(
        #     "INSERT INTO Registration (UUID, BookingName, BookingPhone, SeatsTotal, SeatsOccupied) VALUES (?, ?, ?, ?, ?)",
        #     (uuid_tmp, bname, bmobile, seats_total, "0"),
        # )

    return uuid_tmp


def download_data():
    with create_connection(st.secrets["db_file"]) as conn:
        st.write(conn)  # success message?

        query = conn.execute(f"SELECT * FROM {st.secrets['table_name']}")
        cols = [column[0] for column in query.description]
        results_df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
        st.download_button(
            label="Download Data",
            data=results_df.to_csv(index=False),
            file_name="Registrations.csv",
            mime="text/csv",
        )


def upload_data():
    # https://discuss.streamlit.io/t/uploading-csv-and-excel-files/10866/2
    sqlite_dbs = [file for file in os.listdir(".") if file.endswith(".db")]
    db_filename = st.selectbox("DB Filename", sqlite_dbs)
    table_name = st.text_input("Table Name to Insert")
    conn = create_connection(db_filename)
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # read csv
        try:
            df = pd.read_csv(uploaded_file)
            df.to_sql(name=table_name, con=conn)
            st.write("Data uploaded successfully. These are the first 5 rows.")
            st.dataframe(df.head(5))

        except Exception as e:
            st.write(e)
