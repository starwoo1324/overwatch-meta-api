from flask import Flask, jsonify
import json

app = Flask(__name__)

with open("heroes.json", encoding="utf-8") as f:
    heroes = json.load(f)

@app.route("/")
def home():
    return "Overwatch Meta API Running"

@app.route("/heroes")
def heroes_api():
    return jsonify(heroes)
