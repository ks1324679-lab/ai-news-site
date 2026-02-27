"""
要約済みニュースデータからHTMLサイトを生成するスクリプト
"""
import sys
import os
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from config import DATA_DIR, DOCS_DIR, TEMPLATES_DIR, CATEGORIES


JST = timezone(timedelta(hours=9))


def get_available_dates() -> list[str]:
    """利用可能な日付一覧を取得（新しい順）"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    dates = []
    for f in DATA_DIR.glob("news_*.json"):
        date_str = f.stem.replace("news_", "")
        dates.append(date_str)
    dates.sort(reverse=True)
    return dates[:7]  # 過去7日分まで


def load_news_data(date_str: str) -> dict | None:
    """指定日付のニュースデータを読み込む"""
    filepath = DATA_DIR / f"news_{date_str}.json"
    if not filepath.exists():
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_site():
    """HTMLサイトを生成"""
    print("\n" + "=" * 50)
    print("🌐 Webサイト生成開始")
    print("=" * 50)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    # 利用可能な日付を取得
    dates = get_available_dates()
    if not dates:
        print("⚠ ニュースデータが見つかりません。")
        # デモ用の空データで生成
        dates = [datetime.now(JST).strftime("%Y-%m-%d")]

    # 全日付のデータを読み込み
    all_data = {}
    for date_str in dates:
        data = load_news_data(date_str)
        if data:
            all_data[date_str] = data

    # 日付一覧のJSONを生成
    dates_index = {
        "dates": dates,
        "latest": dates[0] if dates else None,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    index_path = DATA_DIR / "index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(dates_index, f, ensure_ascii=False, indent=2)

    # Jinja2テンプレートからindex.htmlを生成
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("index.html")

    # 最新日のデータをテンプレートに埋め込む
    latest_date = dates[0]
    latest_data = all_data.get(latest_date, {"articles": [], "count": 0})

    html_content = template.render(
        latest_date=latest_date,
        articles=latest_data.get("articles", []),
        count=latest_data.get("count", 0),
        dates=dates,
        categories=CATEGORIES,
        generated_at=datetime.now(JST).strftime("%Y-%m-%d %H:%M"),
    )

    output_path = DOCS_DIR / "index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"  ✓ index.html 生成完了")
    print(f"  ✓ データインデックス生成完了")
    print(f"\n📂 出力先: {DOCS_DIR}")
    print(f"🌐 ブラウザで確認: file:///{DOCS_DIR / 'index.html'}")


if __name__ == "__main__":
    generate_site()
