from flask import Flask, request, jsonify, make_response
import re
import jsonschema
import json
import uuid

############################ Setup ##########################################

# Establish the app
app = Flask(__name__)

# Establsih the app's IP and port it will be running on
APP_IP = '127.0.0.1'
APP_API_PORT = '8080'

# Get the Schemas
with open('data/schemas/receipt_schema.json') as receipt_schema_file:
    RECEIPT_SCHEMA = json.load(receipt_schema_file)

# Memory dedicated for receipt storage
receipts = {}

##############################################################################


# Helper function that returns a Universally Unique IDentifier v4 (UUID4) in str format
def generate_receipt_id():
    return str(uuid.uuid4())

# Helper funtion that adds the given {id: receipt} to the dedicated receipts memory
def add_receipt_by_id(id, receipt):
    """Room for improvement: Locking resources while editing in case of multiple calls"""
    receipts.update({id: receipt})


#################################
# API METHOD: /receipts/process #
#################################
@app.route('/receipts/process', methods=['POST'])
def process_receipts():
    """Room for improvement: Rate limiting and other techniques to aid in high volumes of requests"""

    receipt_data = request.get_json()

    try:
        # Validate the receipt JSON object against the receipt schema
        jsonschema.validate(instance=receipt_data, schema=RECEIPT_SCHEMA)

        # Generate id and add the receipt by id to memory
        id = generate_receipt_id()
        add_receipt_by_id(id, receipt_data)

        return jsonify({'id': id}), 200
    except jsonschema.ValidationError as e:
        # Receipt failed validation, send error
        return make_response(f"Receipt is invalid: {e.message}", 400)
    


if __name__ == '__main__':
    app.run(debug=True, host=APP_IP, port=APP_API_PORT)