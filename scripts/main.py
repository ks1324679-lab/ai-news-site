"""
メインスクリプト - 全処理を順番に実行
fetch_news → summarize → generate_site
"""
import sys
import os

# Windows環境のみUTF-8に設定（Linux/GitHub Actionsでは不要）
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from datetime import datetime, timezone, timedelta

from fetch_news import fetch_all_news, save_raw_articles
from summarize import summarize_articles, save_summarized_articles
from generate_site import generate_site


def main():
    JST = timezone(timedelta(hours=9))
    today = datetime.now(JST).strftime("%Y-%m-%d")

    print("🚀 AIニュース自動収集システム 起動")
    print(f"📅 日付: {today}")
    print()

    # Step 1: ニュース取得
    articles = fetch_all_news()
    if not articles:
        print("\n⚠ 取得できた記事がありません。処理を終了します。")
        return

    save_raw_articles(articles, today)

    # Step 2: Gemini APIで要約
    summarized = summarize_articles(articles)
    save_summarized_articles(summarized, today)

    # Step 3: Webサイト生成
    generate_site()

    print("\n" + "=" * 50)
    print("✅ 全処理完了!")
    print("=" * 50)


if __name__ == "__main__":
    main()
