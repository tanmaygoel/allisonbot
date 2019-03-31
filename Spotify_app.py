from flask import Flask
from flask import render_template

app = Flask(__name__)



@app.route('/')
def index():
    return make_response(open('index.html').read())

if __name__ == "__main__":
    app.run(debug=True)
