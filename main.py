from flask import Flask, request

from models import Payment

app = Flask(__name__)


@app.route('/')
def index():
    return "My first Flask happ."


@app.route('/pay', methods=['POST'])
def pay():
    payment = Payment()


if __name__ == "__main__":
    app.run()
