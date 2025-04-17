from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('dashboard.html')

@app.route('/api/data')
def get_data():
    data_path = os.path.join(app.static_folder, 'data', 'data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/hongkong')
def get_hk_data():
    hk_path = os.path.join(app.static_folder, 'data', 'hongkong.json')
    with open(hk_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True)