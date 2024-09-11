from receipt_processor_main import app
import re
import json

# Generate pattern checking for regex provided on IDs
ID_PATTERN = re.compile("^\\S+$")

################################
# Tests for process_receipts() #
################################
class Test_Process_Receipts:

    # Valid receipts check

    def test_process_receipts__simple_valid_receipt(self):
        with app.test_client() as client:

            ''' ARRANGE '''
            # Using valid simple receipt for data
            with open('data/test_data/simple-receipt.json') as simple_receipt_file:
                simple_receipt = json.load(simple_receipt_file)

            ''' ACT '''
            # Send the POST request to the API /receipts/process
            response = client.post('/receipts/process', json=simple_receipt)

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

    def test_process_receipts__morning_valid_receipt(self):
        with app.test_client() as client:

            ''' ARRANGE '''
            # Using valid morning receipt for data
            with open('data/test_data/morning-receipt.json') as morning_receipt_file:
                morning_receipt = json.load(morning_receipt_file)

            ''' ACT '''
            # Send the POST request to the API /receipts/process
            response = client.post('/receipts/process', json=morning_receipt)

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

    # Missing attributes check

    def test_process_receipts__invalid_simple_receipt_no_retailer(self):
        with app.test_client() as client:

            ''' ARRANGE '''
            with open('data/test_data/simple-receipt_no_retailer.json') as simple_receipt_no_retailer_file:
                simple_receipt_no_retailer = json.load(simple_receipt_no_retailer_file)

            ''' ACT '''
            # Send the POST request to the API /receipts/process
            response = client.post('/receipts/process', json=simple_receipt_no_retailer)

            ''' ASSERT '''
            # Make sure we got the correct status code (ie. 404)
            assert response.status_code == 404, f"{response.data}"

            # Make sure the 'reason the receipt is invalid is for the reason we expect
            assert response.data == b"Receipt is invalid: 'retailer' is a required property"

    def test_process_receipts__invalid_simple_receipt_no_purchaseDate(self):
        with app.test_client() as client:

            ''' ARRANGE '''
            with open('data/test_data/simple-receipt_no_purchaseDate.json') as simple_receipt_no_purchaseDate_file:
                simple_receipt_no_purchaseDate = json.load(simple_receipt_no_purchaseDate_file)

            ''' ACT '''
            # Send the POST request to the API /receipts/process
            response = client.post('/receipts/process', json=simple_receipt_no_purchaseDate)

            ''' ASSERT '''
            # Make sure we got the correct status code (ie. 404)
            assert response.status_code == 404, f"{response.data}"

            # Make sure the 'reason the receipt is invalid is for the reason we expect
            assert response.data == b"Receipt is invalid: 'purchaseDate' is a required property"

    def test_process_receipts__invalid_simple_receipt_no_purchaseTime(self):
        with app.test_client() as client:

            ''' ARRANGE '''
            with open('data/test_data/simple-receipt_no_purchaseTime.json') as simple_receipt_no_purchaseTime_file:
                simple_receipt_no_purchaseTime = json.load(simple_receipt_no_purchaseTime_file)

            ''' ACT '''
            # Send the POST request to the API /receipts/process
            response = client.post('/receipts/process', json=simple_receipt_no_purchaseTime)

            ''' ASSERT '''
            # Make sure we got the correct status code (ie. 404)
            assert response.status_code == 404, f"{response.data}"

            # Make sure the 'reason the receipt is invalid is for the reason we expect
            assert response.data == b"Receipt is invalid: 'purchaseTime' is a required property"

    def test_process_receipts__invalid_simple_receipt_no_total(self):
        with app.test_client() as client:

            ''' ARRANGE '''
            with open('data/test_data/simple-receipt_no_total.json') as simple_receipt_no_total_file:
                simple_receipt_no_total = json.load(simple_receipt_no_total_file)

            ''' ACT '''
            # Send the POST request to the API /receipts/process
            response = client.post('/receipts/process', json=simple_receipt_no_total)

            ''' ASSERT '''
            # Make sure we got the correct status code (ie. 404)
            assert response.status_code == 404, f"{response.data}"

            # Make sure the 'reason the receipt is invalid is for the reason we expect
            assert response.data == b"Receipt is invalid: 'total' is a required property"

    def test_process_receipts__invalid_simple_receipt_no_items(self):
        with app.test_client() as client:

            ''' ARRANGE '''
            with open('data/test_data/simple-receipt_no_items.json') as simple_receipt_no_items_file:
                simple_receipt_no_items = json.load(simple_receipt_no_items_file)

            ''' ACT '''
            # Send the POST request to the API /receipts/process
            response = client.post('/receipts/process', json=simple_receipt_no_items)

            ''' ASSERT '''
            # Make sure we got the correct status code (ie. 404)
            assert response.status_code == 404, f"{response.data}"

            # Make sure the 'reason the receipt is invalid is for the reason we expect
            assert response.data == b"Receipt is invalid: 'items' is a required property"

    def test_process_receipts__invalid_simple_receipt_empty_items(self):
        with app.test_client() as client:

            ''' ARRANGE '''
            with open('data/test_data/simple-receipt_empty_items.json') as simple_receipt_empty_items_file:
                simple_receipt_empty_items = json.load(simple_receipt_empty_items_file)

            ''' ACT '''
            # Send the POST request to the API /receipts/process
            response = client.post('/receipts/process', json=simple_receipt_empty_items)

            ''' ASSERT '''
            # Make sure we got the correct status code (ie. 404)
            assert response.status_code == 404, f"{response.data}"

            # Make sure the 'reason the receipt is invalid is for the reason we expect
            assert response.data == b"Receipt is invalid: [] should be non-empty"

    # Existing but invalid attributes 
    # Note: the json schema does not validate the date or time (so no tests for them here); 
    # it just sets the format as date or time because the .yml only specified format and not pattern

    def test_process_receipts__invalid_simple_receipt_bad_invalid_retailer(self):
        with app.test_client() as client:

            ''' ARRANGE '''
            with open('data/test_data/simple-receipt_invalid_retailer.json') as simple_receipt_invalid_retailer:
                simple_receipt_invalid_retailer = json.load(simple_receipt_invalid_retailer)

            ''' ACT '''
            # Send the POST request to the API /receipts/process
            response = client.post('/receipts/process', json=simple_receipt_invalid_retailer)

            ''' ASSERT '''
            # Make sure we got the correct status code (ie. 404)
            assert response.status_code == 404, f"{response.data}"

            # Make sure the 'reason the receipt is invalid is for the reason we expect
            #assert response.data == b"Receipt is invalid: "

    def test_process_receipts__invalid_simple_receipt_bad_invalid_total(self):
        with app.test_client() as client:

            ''' ARRANGE '''
            with open('data/test_data/simple-receipt_invalid_total.json') as simple_receipt_invalid_total:
                simple_receipt_invalid_total = json.load(simple_receipt_invalid_total)

            ''' ACT '''
            # Send the POST request to the API /receipts/process
            response = client.post('/receipts/process', json=simple_receipt_invalid_total)

            ''' ASSERT '''
            # Make sure we got the correct status code (ie. 404)
            assert response.status_code == 404, f"{response.data}"

            # Make sure the 'reason the receipt is invalid is for the reason we expect
            #assert response.data == b"Receipt is invalid: "