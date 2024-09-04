from flask import Flask, request, jsonify
import re
import jsonschema
import json

# Establish the app
app = Flask(__name__)

# Memory dedicated for receipt storage
receipts = {}

# Get the Schemas
with open('receipt_schema.json') as receipt_schema_file:
    RECEIPT_SCHEMA = json.load(receipt_schema_file)

#################################
# API METHOD: /receipts/process #
#################################
@app.route('/receipts/process', methods=['POST'])
def process_receipts():

    receipt_data = request.get_json()

    try:
        # Validate the JSON object against the schema
        print(jsonschema.validate(instance=receipt_data, schema=RECEIPT_SCHEMA))
        print("Receipt is valid.")
    except jsonschema.ValidationError as e:
        print(f"Receipt is invalid: {e.message}")

    return jsonify({'id': "adb6b560-0eef-42bc-9d16-df48f30e89b2"}) 


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)