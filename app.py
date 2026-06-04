from flask import Flask, jsonify
from bs4 import BeautifulSoup
import json
import requests

app = Flask(__name__)

with open("heroes.json", encoding="utf-8") as f:
    heroes = json.load(f)

@app.route("/")
def home():
    return "Overwatch Meta API Running"

@app.route("/heroes")
def heroes_api():
    return jsonify(heroes)

@app.route("/blizzard-test")
def blizzard_test():
    try:
        url = "https://overwatch.blizzard.com/ko-kr/rates?input=PC&map=all-maps&region=Asia&role=All&rq=1&tier=Master"

        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        return jsonify({
            "success": True,
            "status": response.status_code,
            "length": len(response.text)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/real-heroes")
def real_heroes():
    try:
        url = "https://overwatch.blizzard.com/ko-kr/rates?input=PC&map=all-maps&region=Asia&role=All&rq=1&tier=Master"

        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        soup = BeautifulSoup(response.text, "html.parser")

        return jsonify({
            "success": True,
            "title": soup.title.string if soup.title else "No Title",
            "html_length": len(response.text)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/html-sample")
def html_sample():
    url = "https://overwatch.blizzard.com/ko-kr/rates?input=PC&map=all-maps&region=Asia&role=All&rq=1&tier=Master"

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20
    )

    text = response.text

    return jsonify({
        "hero_count": text.count('"winrate"'),
        "first_dva": text.find('"name":"D.Va"')
    })
