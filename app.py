from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
from html import unescape
import json
import requests
import re

app = Flask(__name__)
CORS(app)

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
        tier = request.args.get("tier", "Master")
        region = request.args.get("region", "Asia")

        url = (
            f"https://overwatch.blizzard.com/ko-kr/rates"
            f"?input=PC"
            f"&map=all-maps"
            f"&region={region}"
            f"&role=All"
            f"&rq=1"
            f"&tier={tier}"
        )

        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        text = unescape(response.text)

        matches = re.findall(
            r'"name":"([^"]+)","winrate":([0-9.]+),"pickrate":([0-9.]+)',
            text
        )
        index = text.find('"name":"D.Va"')

        return jsonify({
        "index": index,
        "sample": text[index:index+1000]
    })

#         heroes = []
#         seen = set()

#         ROLE_MAP = {
#             # 탱커
#             "D.Va": "탱커",
#             "둠피스트": "탱커",
#             "정커퀸": "탱커",
#             "라마트라": "탱커",
#             "라인하르트": "탱커",
#             "로드호그": "탱커",
#             "시그마": "탱커",
#             "윈스턴": "탱커",
#             "레킹볼": "탱커",
#             "자리야": "탱커",
#             "도미나": "탱커",
#             "마우가": "탱커",
#             "오리사": "탱커",
#             "헤저드": "탱커",

#             # 딜러
#             "애쉬": "딜러",
#             "바스티온": "딜러",
#             "캐서디": "딜러",
#             "에코": "딜러",
#             "겐지": "딜러",
#             "한조": "딜러",
#             "정크랫": "딜러",
#             "메이": "딜러",
#             "파라": "딜러",
#             "리퍼": "딜러",
#             "소전": "딜러",
#             "솔저: 76": "딜러",
#             "솜브라": "딜러",
#             "시메트라": "딜러",
#             "토르비욘": "딜러",
#             "트레이서": "딜러",
#             "위도우메이커": "딜러",
#             "벤처": "딜러",
#             "프레야": "딜러",
#             "벤데타": "딜러",
#             "시에라": "딜러",
#             "안란": "딜러",
#             "엠레": "딜러",

#             # 힐러
#             "아나": "힐러",
#             "바티스트": "힐러",
#             "브리기테": "힐러",
#             "일리아리": "힐러",
#             "주노": "힐러",
#             "키리코": "힐러",
#             "라이프위버": "힐러",
#             "루시우": "힐러",
#             "메르시": "힐러",
#             "모이라": "힐러",
#             "젠야타": "힐러",
#             "미즈키": "힐러",
#             "우양": "힐러",
#             "제트팩 캣": "힐러",
#         }

#         for match in matches:
#             hero_name = match[0]

#             if hero_name.lower() == "battlenet":
#                 continue

#             if hero_name not in seen:
#                 seen.add(hero_name)

#                 heroes.append({
#                     "name": hero_name,
#                     "role": ROLE_MAP.get(hero_name, "미정"),
#                     "winrate": float(match[1]),
#                     "pickrate": float(match[2]),
#                 })

#        return jsonify({
#     "tier": tier,
#     "region": region,
#     "sample": matches[:3],
#     "count": len(heroes),
#     "heroes": heroes
# })
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
