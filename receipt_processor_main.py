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

#################################
# API METHOD: /receipts/process #
#################################

# Helper function that returns a Universally Unique IDentifier v4 (UUID4) in str format
def generate_receipt_id() -> str:
    """Room for improvement: Vet the output to match the regex string for IDs"""
    return str(uuid.uuid4())

# Helper funtion that adds the given {id: receipt} to the dedicated receipts memory
def add_receipt_by_id(id, receipt) -> None:
    """Room for improvement: Locking resources while editing in case of multiple calls"""
    receipts.update({id: receipt})

# The actual endpoint
@app.route('/receipts/process', methods=['POST'])
def process_receipts() -> {json,int}:
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
        return make_response(f"Receipt is invalid: {e.message}", 404) # SOF: Maybe remove the message since it's not in the yml

####################################
# API METHOD: /receipts/<id>points #
####################################

# Helper class
class Calculate_Receipt_Points:

    def __init__(self, receipt) -> None:
        self.pointsTotal = 0
        self.retailer = receipt['retailer']
        self.purchaseDate = receipt['purchaseDate']
        self.purchaseTime = receipt['purchaseTime']
        self.total = receipt['total']
        self.items = receipt['items']

    def alphaNumInRetailer(self):
        for letter in self.retailer:
            if(letter.isalnum()):
                self.pointsTotal += 1

    def roundTotal(self):
        pass
    def totalMultipleOf25Cents(self):
        pass
    def twoItemCount(self):
        pass
    def shortDecriptionMultipleOf3(self):
        pass
    def oddDay(self):
        pass
    def timeIs14to16(self):
        pass

@app.route('/receipts/<id>/points', methods=['GET'])
def get_receipt_points(id):

    # Create the class and run the methods desired
    receipt_calc = Calculate_Receipt_Points(receipts[id])
    receipt_calc.alphaNumInRetailer()

    return jsonify({"points": receipt_calc.pointsTotal})


if __name__ == '__main__':
    app.run(debug=True, host=APP_IP, port=APP_API_PORT)