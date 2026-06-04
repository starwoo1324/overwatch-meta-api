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

valid_heroes = [
    "D.Va", "둠피스트", "정커퀸", "라마트라", "라인하르트",
    "로드호그", "시그마", "윈스턴", "레킹볼", "자리야",
    "애쉬", "바스티온", "캐서디", "에코", "겐지",
    "한조", "정크랫", "메이", "파라", "리퍼",
    "소전", "솔저: 76", "솜브라", "시메트라", "토르비욘",
    "트레이서", "위도우메이커", "벤처", "프레야",
    "아나", "바티스트", "브리기테", "일리아리", "주노",
    "키리코", "라이프위버", "루시우", "메르시", "모이라",
    "젠야타"
]

heroes = []

for match in matches:
    if match[0] in valid_heroes:
        heroes.append({
            "name": match[0],
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
