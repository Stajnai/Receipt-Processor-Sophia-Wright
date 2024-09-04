import pytest
from flask import jsonify
from receipt_processor_main import app
import re

APP_IP = '127.0.0.1'
APP_API_PORT = '8080'
ID_PATTERN = re.compile("^\\S+$")

simple_receipt = {
    "retailer": "Target",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "13:13",
    "total": "1.25",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
    ]
}

################################
# Tests for process_receipts() #
################################

def test_process_receipts__simple_valid_receipt():
    with app.test_client() as client:

        ''' ARRANGE '''
        # Using simple receipt for data

        ''' ACT '''
        # Send the POST request to the API /receipts/process
        response = client.post('/receipts/process', json=simple_receipt)

        ''' ASSERT '''

        # Extract the data from the response
        response_data = response.get_json()

        # Make sure we got a good status code (ie. 200)
        assert response.status_code == 200

        # Make sure we have an 'id' property
        assert 'id' in response_data

        # Make sure the 'id' property is a string
        assert isinstance(response_data['id'], str)

        # Make sure the 'id' property is in the right format
        assert ID_PATTERN.match(response_data['id'])

        print(response_data)