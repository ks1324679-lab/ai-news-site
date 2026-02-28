"""
Gemini APIを使ってニュース記事を日本語で要約するスクリプト
"""
import sys
import os
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL, CATEGORIES, DATA_DIR


def create_client():
    """Gemini APIクライアントを作成"""
    if not GEMINI_API_KEY:
        print("⚠ GEMINI_API_KEY が設定されていません。")
        print("  環境変数 GEMINI_API_KEY にAPIキーを設定してください。")
        print("  取得先: https://aistudio.google.com/apikey")
        return None

    client = genai.Client(api_key=GEMINI_API_KEY)
    return client


def summarize_articles(articles: list) -> list:
    """記事リストを日本語で要約・カテゴリ分類する"""
    client = create_client()

    if not client:
        print("⚠ APIクライアント未初期化のため、要約をスキップします。")
        # APIキーがない場合は元の概要をそのまま使用
        for article in articles:
            article["summary_ja"] = article.get("summary_original", "（要約なし）")
            article["title_ja"] = article["title"]
            article["category"] = "その他"
        return articles

    categories_str = "、".join(CATEGORIES)

    print("\n" + "=" * 50)
    print("🤖 Gemini APIで記事を要約中...")
    print("=" * 50)

    summarized = []

    # バッチ処理: 複数記事をまとめて処理
    batch_size = 5
    for i in range(0, len(articles), batch_size):
        batch = articles[i : i + batch_size]

        # バッチ用プロンプト作成
        articles_text = ""
        for idx, article in enumerate(batch):
            articles_text += f"""
--- 記事 {idx + 1} ---
タイトル: {article['title']}
ソース: {article['source']}
言語: {article['language']}
概要: {article.get('summary_original', '（概要なし）')}
URL: {article['url']}
"""

        prompt = f"""以下のAI関連ニュース記事をそれぞれ日本語で要約してください。

## 重要なルール
- **英語の記事は、タイトルと要約を必ず自然な日本語に翻訳してください。**
- 日本語の記事はそのままでOKです。
- 要約は2〜3文（100〜200文字程度）で、記事の核心を簡潔に伝えてください。
- 「生成AI」カテゴリは、画像生成・動画生成・音声/音楽生成・文章生成に関する記事に使ってください。

各記事について以下のJSON形式で出力してください。JSON配列のみを出力し、他のテキストは含めないでください。

[
  {{
    "index": 記事番号（1始まり）,
    "title_ja": "日本語のタイトル（英語記事は翻訳、日本語記事はそのまま）",
    "summary_ja": "2〜3文の日本語要約（100〜200文字程度）",
    "category": "カテゴリ名"
  }}
]

カテゴリは以下から1つ選択: {categories_str}

{articles_text}"""

        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

            response_text = response.text.strip()
            
            import re
            match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if not match:
                raise ValueError(f"レスポンスからJSON配列を抽出できませんでした。\nResponse: {response_text[:200]}...")

            json_str = match.group(0)
            results = json.loads(json_str)

            for result in results:
                idx = result.get("index", 1) - 1
                if 0 <= idx < len(batch):
                    batch[idx]["title_ja"] = result.get("title_ja", batch[idx]["title"])
                    batch[idx]["summary_ja"] = result.get("summary_ja", "（要約取得失敗）")
                    batch[idx]["category"] = result.get("category", "その他")

            summarized.extend(batch)
            msg = f"  ✓ バッチ {i // batch_size + 1}: {len(batch)}件処理完了\n"
            print(msg, end="")
            with open(DATA_DIR / "run_log.txt", "a", encoding="utf-8") as lf: lf.write(msg)

        except json.JSONDecodeError as e:
            msg = f"  ⚠ JSON解析エラー（バッチ {i // batch_size + 1}）: {e}\n  対象文字列: {json_str[:200] if 'json_str' in locals() else 'None'}\n"
            print(msg, end="")
            with open(DATA_DIR / "run_log.txt", "a", encoding="utf-8") as lf: lf.write(msg)
            # フォールバック
            for article in batch:
                article["summary_ja"] = article.get("summary_original", "（要約なし）")
                article["title_ja"] = article["title"]
                article["category"] = "その他"
            summarized.extend(batch)

        except Exception as e:
            msg = f"  ✗ API呼び出しエラー（バッチ {i // batch_size + 1}）: [{type(e).__name__}] {e}\n"
            print(msg, end="")
            with open(DATA_DIR / "run_log.txt", "a", encoding="utf-8") as lf: lf.write(msg)
            for article in batch:
                article["summary_ja"] = article.get("summary_original", "（要約なし）")
                article["title_ja"] = article["title"]
                article["category"] = "その他"
            summarized.extend(batch)

        # レートリミット対策
        if i + batch_size < len(articles):
            time.sleep(5)

    print(f"\n✓ 全{len(summarized)}件の要約完了")
    return summarized


def save_summarized_articles(articles: list, date_str: str) -> Path:
    """要約済み記事をJSONファイルに保存"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 保存用にデータを整形
    output = []
    for article in articles:
        output.append({
            "id": article["id"],
            "title": article.get("title_ja", article["title"]),
            "title_original": article["title"],
            "url": article["url"],
            "summary": article.get("summary_ja", article.get("summary_original", "")),
            "category": article.get("category", "その他"),
            "source": article["source"],
            "language": article["language"],
            "published": article["published"],
            "thumbnail": article.get("thumbnail", ""),
        })

    filepath = DATA_DIR / f"news_{date_str}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({
            "date": date_str,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "count": len(output),
            "articles": output,
        }, f, ensure_ascii=False, indent=2)

    print(f"💾 要約データ保存: {filepath}")
    return filepath


if __name__ == "__main__":
    today = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
    raw_file = DATA_DIR / f"raw_{today}.json"

    if not raw_file.exists():
        print(f"⚠ 生データファイルが見つかりません: {raw_file}")
        print("  先に fetch_news.py を実行してください。")
        exit(1)

    with open(raw_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    summarized = summarize_articles(articles)
    save_summarized_articles(summarized, today)
