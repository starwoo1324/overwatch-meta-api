from flask import Flask, jsonify
from bs4 import BeautifulSoup
from html import unescape
import json
import requests
import re

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

        text = unescape(response.text)

        matches = re.findall(
            r'"name":"([^"]+)".*?"winrate":([0-9.]+).*?"pickrate":([0-9.]+)',
            text,
            re.DOTALL
        )

        heroes = []
        seen = set()

        for match in matches:
            hero_name = match[0]

            if hero_name not in seen:
                seen.add(hero_name)

                heroes.append({
                    "name": hero_name,
                    "winrate": float(match[1]),
                    "pickrate": float(match[2]),
                })

        return jsonify({
            "count": len(heroes),
            "heroes": heroes
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

    text = unescape(response.text)

    return jsonify({
        "hero_count": text.count('"winrate"'),
        "first_dva": text.find('"name":"D.Va"'),
        "contains_dva": '"name":"D.Va"' in text
    })
