import json

from flask import Flask, request, Response
from validator import Validator

app = Flask(__name__)
validate = Validator()


@app.route('/pay', methods=['POST', 'GET'])
def ProcessPayment():
    try:
        valid_data = validate(request)
    except:
        return Response(status=400)


    return Response(status=200)




if __name__ == "__main__":
    app.run(debug=True)
