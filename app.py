from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Vulnerable App is Live!</h1><p>Project by Lakshmi</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)