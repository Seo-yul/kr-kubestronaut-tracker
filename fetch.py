"""Korean Kubestronaut Tracker - CNCF 한국 Kubestronaut 명단 추적기"""

import json
import os
import shutil
from datetime import datetime, timezone, timedelta

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.cncf.io/"
PARAMS_TEMPLATE = {
    "sfid": "105686",
    "sf_action": "get_data",
    "sf_data": "all",
    "_sft_lf-country": "kr",
}
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
THIS_WEEK_FILE = os.path.join(DATA_DIR, "this-week-kr-kubestronaut.json")
LAST_WEEK_FILE = os.path.join(DATA_DIR, "last-week-kr-kubestronaut.json")
NEW_FILE = os.path.join(DATA_DIR, "new-kubestronaut.json")
KST = timezone(timedelta(hours=9))


def parse_person(block) -> dict:
    """person 블록(BeautifulSoup Tag)에서 정보를 추출한다."""
    name_tag = block.select_one(".person__name")
    company_tag = block.select_one(".person__company")
    golden = "golden-kubestronaut" in block.get("class", [])

    linkedin = None
    github = None
    for a in block.select(".person__social a"):
        href = a.get("href", "")
        svg = a.select_one("svg")
        label = svg.get("aria-label", "") if svg else ""
        if "linkedin" in href.lower() or label == "LinkedIn":
            linkedin = href
        elif "github" in href.lower() or label == "GitHub":
            github = href

    return {
        "name": name_tag.get_text(strip=True) if name_tag else "",
        "company": company_tag.get_text(strip=True) if company_tag else "",
        "golden": golden,
        "linkedin": linkedin,
        "github": github,
    }


def fetch_kubstronauts() -> list[dict]:
    """CNCF AJAX API에서 한국 Kubestronaut 전체 명단을 가져온다."""
    all_people = []
    page = 1

    print("Fetching Korean Kubstronauts from CNCF...")

    while True:
        params = {**PARAMS_TEMPLATE, "sf_paged": str(page)}
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        html = data.get("results", "")
        soup = BeautifulSoup(html, "html.parser")
        blocks = soup.select("div.person")

        if not blocks:
            print(f"  Page {page}: 0 people (done)")
            break

        print(f"  Page {page}: {len(blocks)} people")

        for block in blocks:
            person = parse_person(block)
            if person["name"]:
                all_people.append(person)

        page += 1

    print(f"\nTotal: {len(all_people)} kubstronauts fetched")
    return all_people


def compare_and_save():
    """fetch → 저장 → 지난주 데이터와 비교 → 신규 인원 저장."""
    os.makedirs(DATA_DIR, exist_ok=True)

    # 기존 this-week → last-week 로 rotate
    if os.path.exists(THIS_WEEK_FILE):
        shutil.move(THIS_WEEK_FILE, LAST_WEEK_FILE)

    # 새로 fetch
    people = fetch_kubstronauts()
    now = datetime.now(KST).isoformat()

    this_week_data = {
        "fetched_at": now,
        "total": len(people),
        "kubstronauts": people,
    }

    with open(THIS_WEEK_FILE, "w", encoding="utf-8") as f:
        json.dump(this_week_data, f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {THIS_WEEK_FILE}")

    # 비교: last-week 대비 신규 인원
    last_week_names: set[str] = set()
    if os.path.exists(LAST_WEEK_FILE):
        with open(LAST_WEEK_FILE, encoding="utf-8") as f:
            last_data = json.load(f)
        last_week_names = {p["name"] for p in last_data.get("kubstronauts", [])}

    new_people = [p for p in people if p["name"] not in last_week_names]

    new_data = {
        "fetched_at": now,
        "total": len(new_people),
        "kubstronauts": new_people,
    }
    with open(NEW_FILE, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

    # 출력
    if last_week_names:
        print(f"\n📋 New Kubstronauts (compared to last week): {len(new_people)}")
    else:
        print(f"\n📋 First run — all {len(new_people)} kubstronauts listed as new")

    for i, p in enumerate(new_people, 1):
        print(f"  {i}. {p['name']} ({p['company']})")

    print(f"\nSaved: {NEW_FILE}")


if __name__ == "__main__":
    compare_and_save()
