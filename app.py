from flask import Flask, jsonify

app = Flask(__name__)

heroes = [
    {
        "name": "시그마",
        "role": "탱커",
        "winRate": 52.3,
        "pickRate": 4.2
    },
    {
        "name": "주노",
        "role": "힐러",
        "winRate": 51.3,
        "pickRate": 6.8
    }
]

@app.route("/")
def home():
    return "Overwatch Meta API Running"

@app.route("/heroes")
def heroes_api():
    return jsonify(heroes)
