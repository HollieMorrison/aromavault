from flask import Flask, jsonify
app = Flask(__name__)
@app.get('/')
def home():
    return '<h1>AromaVault</h1><p>App deployed successfully!</p>'
@app.get('/health')
def health():
    return jsonify({'status': 'ok'})
