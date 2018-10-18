from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def lindex():
    return "My first Flask happ."


if __name__ == "__main__":
    app.run()
