import json

from flask import Flask, request, Response

from models import Payment
from validator import Validator

app = Flask(__name__)
validate = Validator()


@app.route('/pay', methods=['POST', 'GET'])
def ProcessPayment():
    try:
        valid_data = validate(request)
    except:
        return Response(status=400)

    payment = Payment(valid_data)
    try:
        payment.execute_payment()
    except Exception as e:
        return Response(e.__str__(), status=400)

    return Response(status=200)


if __name__ == "__main__":
    app.run(debug=True)
