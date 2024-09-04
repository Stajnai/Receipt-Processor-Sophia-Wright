from receipt_processor_main import app
import re
import json

ID_PATTERN = re.compile("^\\S+$")

with open('data/test_data/simple-receipt.json') as simple_receipt_file:
    SIMPLE_RECEIPT = json.load(simple_receipt_file)


################################
# Tests for process_receipts() #
################################

def test_process_receipts__simple_valid_receipt():
    with app.test_client() as client:

        ''' ARRANGE '''
        # Using simple receipt for data

        ''' ACT '''
        # Send the POST request to the API /receipts/process
        response = client.post('/receipts/process', json=SIMPLE_RECEIPT)

        ''' ASSERT '''

        # Extract the data from the response
        response_data = response.get_json()

        # Make sure we got a good status code (ie. 200)
        assert response.status_code == 200, f"{response.data}"

        # Make sure we have an 'id' property
        assert 'id' in response_data

        # Make sure the 'id' property is a string
        assert isinstance(response_data['id'], str)

        # Make sure the 'id' property is in the right format
        assert ID_PATTERN.match(response_data['id'])