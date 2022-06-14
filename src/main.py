""" Python modules
    logging: logs
    fastapi: Fastapi Framework
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.models import Address

logging.basicConfig(level=logging.INFO, filename="logs/db_connection.log",
                    format=" %(asctime)s - %(levelname)s - %(message)s")


app = FastAPI()


class UserAddress(BaseModel):
    """
    Schema for UserAddress

    """
    address_name: str = ''
    coordinates: str = ''


@app.post("/createAddress")
async def create_address(address: UserAddress):
    """
    Create address as per the User given

    E.x:
    {
        "address_name":"#2180 Bhaji Market",
        "coordinates":"21.21, 22.22"
    }

    """
    latitude, longitude = address.coordinates.split(",")

    # validate the coordinates
    validation_response = validate_address(latitude, longitude)

    if validation_response == 1405:
        logging.error("Enter a Valid location: Latitude is out of range")
        raise HTTPException(status_code=400,
                detail="Enter a Valid location: Latitude is out of range")

    if validation_response == 1406:
        logging.error("Enter a Valid location: Longitude is out of range")
        raise HTTPException(status_code=400,
                detail="Enter a Valid location: Longitude is out of range")

    if validation_response == 1407:
        logging.error("Both Latitude and Longitude are out of range")
        raise HTTPException(status_code=400,
                detail="Both Latitude and Longitude are out of range")

    address_table = Address(address.address_name, address.coordinates)
    address_response = address_table.create_address()

    if address_response == 1500:
        raise HTTPException(status_code=400,
                detail="Address ID already exists - \
                Please Enter the Unique Address Name")


    return JSONResponse(content="User Address added successfully",
                        media_type="application/text",
                        status_code=200)


@app.delete("/deleteAddress/")
async def delete_address_by_name(address_name: str):
    """
    Delete Address by name

    E.x: http://127.0.0.1:8000/deleteAddress/?address_name='Bangalore street'

    """
    addr = Address()
    if not addr.delete_address(query_address_name=address_name):
        raise HTTPException(status_code=404,
                detail="Enter a valid address name")

    return JSONResponse(content="Successfully deleted the address",
                        media_type="application/text",
                        status_code=200)


@app.get("/getAllAddresses")
async def get_all_addresses():
    """
    get all addresses from database
    """
    address_table = Address()
    res = address_table.get_address_ids()

    return JSONResponse(content=res,
                            media_type="application/json",
                            status_code=200)


@app.put("/updateAddress")
async def update_address(address: UserAddress):
    """
    Update the userAddress

    """

    latitude, longitude = address.coordinates.split(",")

    # validate the coordinates
    validation_response = validate_address(latitude, longitude)

    if validation_response == 1405:
        logging.error("Enter a Valid location: Latitude is out of range")
        raise HTTPException(status_code=400,
                detail="Enter a Valid location: Latitude is out of range")

    if validation_response == 1406:
        logging.error("Enter a Valid location: Longitude is out of range")
        raise HTTPException(status_code=400,
                detail="Enter a Valid location: Longitude is out of range")

    if validation_response == 1407:
        logging.error("Both Latitude and Longitude are out of range")
        raise HTTPException(status_code=400,
                detail="Both Latitude and Longitude are out of range")

    address_table = Address(address.address_name, address.coordinates)
    update_response = address_table.update_address()

    if update_response == 1500:
        raise HTTPException(status_code=404,
                detail="No Data found for the given address name")

    return JSONResponse(content="User Address Updated successfully",
                        media_type="application/text",
                        status_code=200)


@app.get("/getAddressWithinRange")
async def get_address_within_range(rang: int, location: str):
    """
    Get address within range

    E.x:
        API: http://127.0.0.1:8000/getAddressWithinRange/?range=value&location=val1,val2


        http://127.0.0.1:8000/getAddressWithinRange/?range=200&location=15.92,74.40
        http://127.0.0.1:8000/getAddressWithinRange/?range=100&location=72.85,85.26
        (range in kms)

    """
    addr = Address()
    addresses_from_db = addr.get_address_in_range(rang, location)
    response = []

    if not addresses_from_db:
        raise HTTPException(status_code=404,
                detail="No Address found within the range")

    for each_address in addresses_from_db:
        response.append(each_address)

    return response


def validate_address(latitude, longitude):
    """
    The latitude value should be within range of -90 to +90 degress
    The longiutude value should be within range of -180 to +180 degress
    Naming Error Convention:
        1405: Latitude out of range
        1406: Longitude out of range
        1407: Both lat and long are out of range
    """
    lat = 0
    long = 0

    # Latitude Check
    if float(latitude) < -90 or float(latitude) > 90:
        lat = 1405

    # Longitude Check
    if float(longitude) < -180 or float(longitude) > 180:
        long = 1406

    if lat and long:
        return 1407

    if lat:
        return lat
    if long:
        return long

    return True
