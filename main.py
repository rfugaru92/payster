from flask import Flask, request, Response, render_template, redirect

from models import Payment
from validator import Validator

app = Flask(__name__)
validate = Validator()


@app.route('/pay', methods=['POST', 'GET'])
def ProcessPayment():
    if request.method == "GET":
        return render_template("pay.html")
    else:
        try:
            valid_data = validate(request)
        except Exception as e:
            return Response(e.__str__(), status=400)

        payment = Payment(valid_data)
        try:
            payment.execute_payment()
        except Exception as e:
            return Response(e.__str__(), status=400)

        return Response("Payment was successful.<br><a href='/pay'>New payment'</a>", status=200)


if __name__ == "__main__":
    app.run(debug=True)
