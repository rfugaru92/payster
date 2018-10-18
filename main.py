from flask import Flask, request, Response
import json
from models import Payment
from validator import Validator

app = Flask(__name__)
validate = Validator()


@app.route('/pay', methods=['POST', 'GET'])
def ProcessPayment():
    try:
        valid_data = validate(request)
        print(valid_data)
        return Response('E bine', status=200, mimetype="application/text")
    except:
        return Response(status=400)


if __name__ == "__main__":
    app.run(debug=True)
