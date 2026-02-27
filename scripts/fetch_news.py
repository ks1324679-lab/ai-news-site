"""
RSSフィードからAIニュースを収集するスクリプト
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path

import feedparser
from dateutil import parser as date_parser

from config import RSS_FEEDS, MAX_ARTICLES_PER_FEED, MAX_TOTAL_ARTICLES, HOURS_LOOKBACK, DATA_DIR


def fetch_feed(feed_info: dict) -> list[dict]:
    """1つのRSSフィードから記事を取得する"""
    articles = []
    try:
        print(f"  取得中: {feed_info['name']}...")
        feed = feedparser.parse(feed_info["url"])

        if feed.bozo and not feed.entries:
            print(f"  ⚠ フィード解析エラー: {feed_info['name']}")
            return []

        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=HOURS_LOOKBACK)

        for entry in feed.entries[:MAX_ARTICLES_PER_FEED]:
            # 公開日時の解析
            published = None
            for date_field in ["published", "updated", "created"]:
                if hasattr(entry, date_field) and getattr(entry, date_field):
                    try:
                        published = date_parser.parse(getattr(entry, date_field))
                        if published.tzinfo is None:
                            published = published.replace(tzinfo=timezone.utc)
                        break
                    except (ValueError, TypeError):
                        continue

            # 日時がない場合はスキップせず取得（最新記事の可能性あり）
            if published and published < cutoff_time:
                continue

            # 概要の取得
            summary = ""
            if hasattr(entry, "summary"):
                summary = entry.summary
            elif hasattr(entry, "description"):
                summary = entry.description

            # HTMLタグの簡易除去
            import re
            summary = re.sub(r"<[^>]+>", "", summary).strip()
            # 長すぎる概要を切り詰め
            if len(summary) > 500:
                summary = summary[:500] + "..."

            # 記事IDの生成（URLベースのハッシュ）
            article_id = hashlib.md5(entry.link.encode()).hexdigest()[:12]

            articles.append({
                "id": article_id,
                "title": entry.title,
                "url": entry.link,
                "summary_original": summary,
                "published": published.isoformat() if published else datetime.now(timezone.utc).isoformat(),
                "source": feed_info["name"],
                "language": feed_info["language"],
            })

        print(f"  ✓ {feed_info['name']}: {len(articles)}件取得")

    except Exception as e:
        print(f"  ✗ {feed_info['name']}でエラー: {e}")

    return articles


def deduplicate_articles(articles: list[dict]) -> list[dict]:
    """タイトルの類似度で重複記事を排除"""
    seen_titles = set()
    unique_articles = []

    for article in articles:
        # タイトルを正規化して比較
        normalized = article["title"].lower().strip()
        if normalized not in seen_titles:
            seen_titles.add(normalized)
            unique_articles.append(article)

    return unique_articles


def fetch_all_news() -> list[dict]:
    """全フィードからニュースを取得"""
    print("=" * 50)
    print("📰 AIニュース取得開始")
    print("=" * 50)

    all_articles = []

    for feed_info in RSS_FEEDS:
        articles = fetch_feed(feed_info)
        all_articles.extend(articles)

    # 重複排除
    all_articles = deduplicate_articles(all_articles)

    # 公開日時でソート（新しい順）
    all_articles.sort(key=lambda x: x["published"], reverse=True)

    # 最大件数に制限
    all_articles = all_articles[:MAX_TOTAL_ARTICLES]

    print(f"\n合計: {len(all_articles)}件のユニーク記事を取得")
    return all_articles


def save_raw_articles(articles: list[dict], date_str: str) -> Path:
    """取得した記事をJSONファイルに保存"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_DIR / f"raw_{date_str}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"💾 保存完了: {filepath}")
    return filepath


if __name__ == "__main__":
    today = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
    articles = fetch_all_news()
    if articles:
        save_raw_articles(articles, today)
    else:
        print("⚠ 取得できた記事がありません")
