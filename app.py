from flask import Flask, jsonify, render_template
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__=='__main__':
    app.run(host="localhost", port=5000)