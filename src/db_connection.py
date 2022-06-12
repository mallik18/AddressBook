""" Python modules
    sqlite3: Database
    logging: logs

"""
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, filename="logs/db_connection.log",
                    format=" %(asctime)s - %(levelname)s - %(message)s")


def database_connection_cursor():
    """
    Sqlite Database connection
    """
    try:
        db_conn = sqlite3.connect('AddressBook.db')

        if db_conn:
            logging.info("Success")
            db_curr = db_conn.cursor()

            db_curr.execute("""
                        CREATE TABLE IF NOT EXISTS address_book (
                            address_name TEXT PRIMARY KEY NOT NULL,
                            coordinates TEXT
                            )
                        """)
            return (db_conn, db_curr)

    except sqlite3.Error as err:
        logging.error(err)
