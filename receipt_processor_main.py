from flask import Flask, jsonify
import re
import jsonschema

# Establish the app
app = Flask(__name__)

# Some globals as defined by the yaml
RETAILER_PATTERN = "^[\\w\\s\\-&]+$"
DATE_PATTERN = "((19|20)\d{2}-(0[1-9]|1[1,2])-(0[1-9]|[12][0-9]|3[01]))" # Assuming YYYY-MM-DD
TIME_PATTERN = "((0[0-9]|10-23):(0[0-9]|10-59))"
TOTAL_PATTERN = "^\\d+\\.\\d{2}$"
SHORT_DESC_PATTERN = "^[\\w\\s\\-]+$"
PRICE_PATTERN = TOTAL_PATTERN # The same as TOTAL_PATERN, but including this to be explicit in case any change is desired 

# Memory dedicated for receipt storage
receipts = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipts():

    required_receipt_properties = ['retailer', 'purchaseDate', 'purchaseTime','items', 'total']

    return jsonify({'id': "adb6b560-0eef-42bc-9d16-df48f30e89b2"})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)