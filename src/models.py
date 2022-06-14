""" Python modules
    logging: logs
    geodesic: distance between 2 points
"""
import logging
import sqlite3
from geopy.distance import geodesic


from src.db_connection import database_connection_cursor

logging.basicConfig(level=logging.INFO, filename="logs/db_connection.log",
                    format=" %(asctime)s - %(levelname)s - %(message)s")


# Connecting database and receiving conn and cursor object
db_conn, db_curr = database_connection_cursor()


class Address:
    """
    Address class for UserAddress
    """
    def __init__(self, address_name=None, coordinates=None):
        self.address_name = address_name
        self.coordinates = coordinates

    def create_address(self):
        """
        Method to create/add address into Database
        Error Convention:
            1500: same address_name
        """

        addrs = set()
        ids = self.get_address_ids()
        for addr in ids:
            addrs.add(addr[0])
        if self.address_name in addrs:
            return 1500

        del addrs

        query = f""" INSERT INTO address_book VALUES
                ('{self.address_name}','{self.coordinates}')"""

        try:
            logging.info(db_curr.execute(query))
        except sqlite3.Error as err:
            logging.error(err)

        self.commit()

        return True

    def delete_address(self, query_address_name):
        """Method to delete a address in the DB by name
        """
        addrs = set()
        ids = self.get_address_ids()

        for addr in ids:
            addrs.add(addr[0])

        if query_address_name not in addrs:
            return False
        del addrs

        query = f"""
                    DELETE FROM address_book WHERE
                    address_name ='{query_address_name}';
                """
        try:
            db_curr.execute(query)
            self.commit()
            return True
        except sqlite3.Error as err:
            logging.error(err)

    def update_address(self):
        """Method to update a address in the DB
        """
        addrs = set()
        ids = self.get_address_ids()
        for addr in ids:
            addrs.add(addr[0])

        if self.address_name not in addrs:
            return 1500

        del addrs
        query = f"""
                    UPDATE address_book
                    SET coordinates = '{self.coordinates}'
                    WHERE address_name = '{self.address_name}';
                """

        try:
            logging.info(db_curr.execute(query))

        except sqlite3.Error as err:
            logging.error(err)

        self.commit()

        return True

    def get_address_in_range(self, rang, location):
        """
        Method to get the addresses within the given distance
        and location from sqlite database

        """
        location = location.split(",")
        latitude = float(location[0].strip())
        longitude = float(location[1].strip())

        point = (latitude, longitude)

        addresses_within_range = []
        all_addresses = self.get_address_ids()

        for address in all_addresses:
            address_point = address[1].split(",")
            address_point = (float(address_point[0]), float(address_point[1]))

            diff = geodesic(point, address_point)
            logging.info(f"Location:{location}")
            logging.info(f"Address point: {address_point} -- \
                    Range:{range} -- Difference: {diff}")

            if diff <= rang:
                addresses_within_range.append(address)

        return addresses_within_range

    @staticmethod
    def commit():
        """
        Method to commit the changes done on the database

        """
        db_conn.commit()

    @staticmethod
    def close():
        """
        Method to close the database connection
        """
        db_conn.close()

    @staticmethod
    def get_address_ids():
        """
        Method to get all the address names present in the DB
        """
        try:
            db_curr.execute("""SELECT address_name, coordinates
                                FROM address_book;""")
            rows = db_curr.fetchall()
            return rows
        except sqlite3.Error as err:
            logging.error(err)
