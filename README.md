# API for AddressBook to store address

# File Structure:
    AdreessBook:
        - src:
            - main.py: main logic for API
            - models.py : databasse related logic
            - db_connection.py: database connection
        - logs:
            - db_connection.log: log of whole project


# Python Version - 3.8.10

1. Create a virtual environment:
    if already venv or virtual environment is present delete it
    $ python3 -m venv venv

2. Activate virtual environment:
    $ source venv/bin/activate

3. Install Dependencies:
    $ pip install -r requirements.txt

4. Run server:
    $ uvicorn src.main:app

5. Delete the AddressBook.db file to reset Database.

# Docs can be found in below URL:
http://127.0.0.1:8000/docs

# API endpoints:
1. Crearte/Add address
        Method: POST
        API: http://127.0.0.1:8000/createAddress
        Body: {raw/json} 
            {
                "address_name": "Belgaum",
                "coordinates": "15.92,74.40"
            }
2. Delete address by name
        Method: DELETE
        API: http://127.0.0.1:8000/deleteAddress/?address_name='Bangalore street'

3. Get all addresses present in the address book
        Method: GET
        API: http://127.0.0.1:8000/getAllAddresses


4. Update address by name
        Method: PUT
        API: http://127.0.0.1:8000/updateAddress
        Body:
        {
            "address_name": "Mysore street",
            "coordinates": "11.21, 13.14"
        }

5. Get address within the range
        Method: GET
        API: http://127.0.0.1:8000/getAddressWithinRange/?range=val&location=val1,val2
        *Range in kilometers
        
        E.x:
        http://127.0.0.1:8000/getAddressWithinRange/?range=200&location=15.92,74.40
        http://127.0.0.1:8000/getAddressWithinRange/?range=100&location=72.85,85.26

