from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
from html import unescape
import json
import requests
import re

app = Flask(__name__)
CORS(app)

try:
    with open("heroes.json", encoding="utf-8") as f:
        heroes = json.load(f)
except FileNotFoundError:
    heroes = []


ROLE_MAP = {
    # 탱커
    "D.Va": "탱커",
    "둠피스트": "탱커",
    "정커퀸": "탱커",
    "라마트라": "탱커",
    "라인하르트": "탱커",
    "로드호그": "탱커",
    "시그마": "탱커",
    "윈스턴": "탱커",
    "레킹볼": "탱커",
    "자리야": "탱커",
    "도미나": "탱커",
    "마우가": "탱커",
    "오리사": "탱커",
    "해저드": "탱커",
    "헤저드": "탱커",

    # 딜러
    "애쉬": "딜러",
    "바스티온": "딜러",
    "캐시디": "딜러",
    "캐서디": "딜러",
    "에코": "딜러",
    "겐지": "딜러",
    "한조": "딜러",
    "정크랫": "딜러",
    "메이": "딜러",
    "파라": "딜러",
    "리퍼": "딜러",
    "소전": "딜러",
    "솔저: 76": "딜러",
    "솜브라": "딜러",
    "시메트라": "딜러",
    "토르비욘": "딜러",
    "트레이서": "딜러",
    "위도우메이커": "딜러",
    "벤처": "딜러",
    "프레야": "딜러",
    "벤데타": "딜러",
    "시에라": "딜러",
    "안란": "딜러",
    "엠레": "딜러",

    # 힐러
    "아나": "힐러",
    "바티스트": "힐러",
    "브리기테": "힐러",
    "일리아리": "힐러",
    "주노": "힐러",
    "키리코": "힐러",
    "라이프위버": "힐러",
    "루시우": "힐러",
    "메르시": "힐러",
    "모이라": "힐러",
    "젠야타": "힐러",
    "미즈키": "힐러",
    "우양": "힐러",
    "제트팩 캣": "힐러",
}


COUNTER_DATA = {
    "D.Va": (["윈스턴", "파라"], ["자리야", "메이"], ["감시 기지: 지브롤터", "눔바니"]),
    "디바(D.Va)": (["윈스턴", "파라"], ["자리야", "메이"], ["감시 기지: 지브롤터", "눔바니"]),
    "둠피스트": (["위도우메이커", "아나"], ["솜브라", "오리사"], ["리장 타워", "일리오스"]),
    "윈스턴": (["위도우메이커", "겐지"], ["리퍼", "로드호그"], ["감시 기지: 지브롤터", "뉴 퀸 스트리트"]),
    "라인하르트": (["자리야", "솔저: 76"], ["라마트라", "바스티온"], ["왕의 길", "아이헨발데"]),
    "시그마": (["오리사", "마우가"], ["라인하르트", "시메트라"], ["서킷 로얄", "하바나"]),
    "오리사": (["둠피스트", "라인하르트"], ["시그마", "한조"], ["일리오스", "네팔"]),
    "로드호그": (["윈스턴", "둠피스트"], ["아나", "리퍼"], ["일리오스", "리장 타워"]),
    "자리야": (["D.Va", "겐지"], ["라인하르트", "바스티온"], ["왕의 길", "리장 타워"]),
    "겐지": (["위도우메이커", "한조"], ["메이", "자리야"], ["할리우드", "네팔"]),
    "리퍼": (["윈스턴", "로드호그"], ["파라", "위도우메이커"], ["리장 타워", "일리오스"]),
    "트레이서": (["위도우메이커", "아나"], ["캐시디", "토르비욘"], ["뉴 퀸 스트리트", "일리오스"]),
    "파라": (["정크랫", "리퍼"], ["솔저: 76", "애쉬"], ["리알토", "오아시스"]),
    "솜브라": (["둠피스트", "레킹볼"], ["브리기테", "캐시디"], ["수라바사", "뉴 정크 시티"]),
    "애쉬": (["파라", "겐지"], ["위도우메이커", "둠피스트"], ["할리우드", "블리자드 월드"]),
    "캐시디": (["트레이서", "솜브라"], ["위도우메이커", "한조"], ["미드타운", "왕의 길"]),
    "캐서디": (["트레이서", "솜브라"], ["위도우메이커", "한조"], ["미드타운", "왕의 길"]),
    "소전": (["솔저: 76"], ["위도우메이커"], ["뉴 퀸 스트리트", "콜로세오"]),
    "위도우메이커": (["파라", "애쉬"], ["윈스턴", "겐지"], ["서킷 로얄", "하바나"]),
    "솔저: 76": (["파라", "메르시"], ["시그마", "위도우메이커"], ["눔바니", "에스페란사"]),
    "메이": (["D.Va", "로드호그"], ["파라", "솔저: 76"], ["남극 반도", "리장 타워"]),
    "아나": (["로드호그", "마우가"], ["키리코", "겐지"], ["왕의 길", "아이헨발데"]),
    "바티스트": (["파라"], ["겐지", "트레이서"], ["서킷 로얄", "미드타운"]),
    "루시우": (["위도우메이커"], ["캐시디"], ["일리오스", "리장 타워"]),
    "젠야타": (["로드호그", "탱커진"], ["솜브라", "트레이서"], ["하바나", "서킷 로얄"]),
    "키리코": (["아나", "정커퀸"], ["트레이서"], ["콜로세오", "일리오스"]),
    "메르시": ([], ["솔저: 76", "위도우메이커"], ["눔바니", "도라도"]),
    "모이라": (["겐지", "트레이서"], ["아나", "D.Va"], ["콜로세오", "네팔"]),
    "주노": (["솔저: 76"], ["위도우메이커"], ["루나사피", "왕의 길"]),
    "해저드": (["위도우메이커"], ["아나"], ["부산", "일리오스"]),
    "헤저드": (["위도우메이커"], ["아나"], ["부산", "일리오스"]),
    "레킹볼": (["위도우메이커"], ["솜브라"], ["일리오스", "리장 타워"]),
    "정커퀸": (["로드호그"], ["아나"], ["콜로세오", "뉴 퀸 스트리트"]),
    "라마트라": (["라인하르트"], ["바스티온"], ["왕의 길", "미드타운"]),
    "마우가": (["윈스턴"], ["아나"], ["하바나", "도라도"]),
    "벤처": (["위도우메이커"], ["파라"], ["네팔", "리장 타워"]),
    "에코": (["바스티온"], ["캐시디"], ["도라도", "하바나"]),
    "한조": (["파라"], ["윈스턴"], ["하바나", "서킷 로얄"]),
    "바스티온": (["라인하르트"], ["겐지"], ["하바나", "미드타운"]),
    "정크랫": (["자리야"], ["파라"], ["아이헨발데", "왕의 길"]),
    "시메트라": (["D.Va"], ["파라"], ["왕의 길", "미드타운"]),
    "토르비욘": (["트레이서"], ["파라"], ["아이헨발데", "할리우드"]),
    "브리기테": (["트레이서"], ["파라"], ["리장 타워", "왕의 길"]),
    "라이프위버": (["로드호그"], ["솜브라"], ["왕의 길", "도라도"]),
    "일리아리": (["파라"], ["윈스턴"], ["하바나", "도라도"]),
}


MAP_SLUGS = {
    "전체 맵": "all-maps",
    "all-maps": "all-maps",
    "남극 반도": "antarctic-peninsula",
    "부산": "busan",
    "일리오스": "ilios",
    "리장 타워": "lijiang-tower",
    "네팔": "nepal",
    "오아시스": "oasis",
    "사모아": "samoa",
    "서킷 로얄": "circuit-royal",
    "도라도": "dorado",
    "하바나": "havana",
    "정크타운": "junkertown",
    "리알토": "rialto",
    "66번 국도": "route-66",
    "샴발리 수도원": "shambali-monastery",
    "감시 기지: 지브롤터": "watchpoint-gibraltar",
    "지브롤터": "watchpoint-gibraltar",
    "블리자드 월드": "blizzard-world",
    "아이헨발데": "eichenwalde",
    "할리우드": "hollywood",
    "왕의 길": "kings-row",
    "미드타운": "midtown",
    "눔바니": "numbani",
    "파라이소": "paraiso",
    "콜로세오": "colosseo",
    "에스페란사": "esperanca",
    "뉴 퀸 스트리트": "new-queen-street",
    "루나사피": "runasapi",
    "아틀리스": "aatlis",
    "뉴 정크 시티": "new-junk-city",
    "수라바사": "suravasa",
    "하나오카": "hanaoka",
}


def clean_map_name(map_name):
    map_name = (map_name or "전체 맵").strip()
    return re.sub(r"\s*\([^)]*\)\s*$", "", map_name)


def to_blizzard_map_slug(map_name):
    clean_name = clean_map_name(map_name)
    return MAP_SLUGS.get(clean_name, clean_name if clean_name else "all-maps")


def fetch_rates(tier, region, map_slug):
    url = "https://overwatch.blizzard.com/ko-kr/rates"
    response = requests.get(
        url,
        params={
            "input": "PC",
            "map": map_slug,
            "region": region,
            "role": "All",
            "rq": "1",
            "tier": tier,
        },
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )
    response.raise_for_status()
    return unescape(response.text)


def parse_heroes(text, tier, map_name):
    matches = re.findall(
        r'"name":"([^"]+)","winrate":([0-9.]+),"pickrate":([0-9.]+)',
        text,
    )

    result = []
    seen = set()
    clean_name = clean_map_name(map_name)
    data_map_name = "전체 맵" if clean_name in ("", "전체 맵", "all-maps") else clean_name
    rate_key = f"{tier}-{data_map_name}"

    for hero_name, winrate, pickrate in matches:
        if hero_name.lower() == "battlenet" or hero_name in seen:
            continue

        seen.add(hero_name)
        counters, countered_by, best_maps = COUNTER_DATA.get(hero_name, ([], [], []))
        winrate_value = float(winrate)
        pickrate_value = float(pickrate)

        result.append({
            "name": hero_name,
            "role": ROLE_MAP.get(hero_name, "미정"),
            "winrate": winrate_value,
            "pickrate": pickrate_value,
            "counters": counters,
            "counteredBy": countered_by,
            "bestMaps": best_maps,
            "tierMapWinRates": {rate_key: winrate_value},
            "tierMapPickRates": {rate_key: pickrate_value},
        })

    return result


@app.route("/")
def home():
    return "Overwatch Meta API Running"


@app.route("/heroes")
def heroes_api():
    return jsonify(heroes)


@app.route("/blizzard-test")
def blizzard_test():
    try:
        text = fetch_rates("Master", "Asia", "all-maps")
        return jsonify({
            "success": True,
            "length": len(text),
            "hero_count": text.count('"winrate"'),
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/real-heroes")
def real_heroes():
    try:
        tier = request.args.get("tier", "Master")
        region = request.args.get("region", "Asia")
        map_name = request.args.get("map", "전체 맵")
        map_slug = to_blizzard_map_slug(map_name)

        text = fetch_rates(tier, region, map_slug)
        parsed = parse_heroes(text, tier, map_name)

        if not parsed and map_slug != "all-maps":
            map_slug = "all-maps"
            map_name = "전체 맵"
            text = fetch_rates(tier, region, map_slug)
            parsed = parse_heroes(text, tier, map_name)

        return jsonify({
            "tier": tier,
            "region": region,
            "map": clean_map_name(map_name),
            "mapSlug": map_slug,
            "count": len(parsed),
            "heroes": parsed,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/html-sample")
def html_sample():
    tier = request.args.get("tier", "Master")
    region = request.args.get("region", "Asia")
    map_name = request.args.get("map", "전체 맵")
    map_slug = to_blizzard_map_slug(map_name)
    text = fetch_rates(tier, region, map_slug)

    return jsonify({
        "map": clean_map_name(map_name),
        "mapSlug": map_slug,
        "hero_count": text.count('"winrate"'),
        "first_dva": text.find('"name":"D.Va"'),
        "contains_dva": '"name":"D.Va"' in text,
    })


if __name__ == "__main__":
    app.run(debug=True)
