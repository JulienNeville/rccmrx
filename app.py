from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/architecture', methods=['POST', 'GET'])
def architecture():
    return render_template('architecture.html')