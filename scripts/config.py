"""
設定ファイル - AIニュース自動収集システム
"""
import os

# Gemini API設定
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"

# RSSフィード一覧（AI分野）
RSS_FEEDS = [
    # --- 生成AI特化ソース（画像・動画・音楽生成） ---
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
        "language": "en",
    },
    {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml",
        "language": "en",
    },
    {
        "name": "The Decoder",
        "url": "https://the-decoder.com/feed/",
        "language": "en",
    },
    {
        "name": "MarkTechPost",
        "url": "https://www.marktechpost.com/feed/",
        "language": "en",
    },
    {
        "name": "AI News",
        "url": "https://www.artificialintelligence-news.com/feed/",
        "language": "en",
    },
    {
        "name": "Ledge.ai",
        "url": "https://ledge.ai/feed",
        "language": "ja",
    },
    # --- 総合AIニュース ---
    {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "language": "en",
    },
    {
        "name": "The Verge AI",
        "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "language": "en",
    },
    {
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/",
        "language": "en",
    },
    {
        "name": "Ars Technica AI",
        "url": "https://feeds.arstechnica.com/arstechnica/technology-lab",
        "language": "en",
    },
    {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
        "language": "en",
    },
    {
        "name": "ITmedia AI+",
        "url": "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
        "language": "ja",
    },
    {
        "name": "GIGAZINE",
        "url": "https://gigazine.net/news/rss_2.0/",
        "language": "ja",
    },
    {
        "name": "Google AI Blog",
        "url": "http://feeds.feedburner.com/blogspot/gJZg",
        "language": "en",
    },
    {
        "name": "AI-SCHOLAR",
        "url": "https://ai-scholar.tech/feed",
        "language": "ja",
    },
]

# 取得設定
MAX_ARTICLES_PER_FEED = 5  # 1フィードあたりの最大記事数
MAX_TOTAL_ARTICLES = 40     # 合計最大記事数（フィード増加に合わせて拡大）
HOURS_LOOKBACK = 48         # 過去何時間の記事を取得するか

# ファイルパス
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
DATA_DIR = DOCS_DIR / "data"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# カテゴリ一覧（創作系生成AIを細分化）
CATEGORIES = [
    "画像生成AI",
    "動画生成AI",
    "音楽・音声AI",
    "テキスト生成AI",
    "研究・論文",
    "プロダクト・サービス",
    "ビジネス・企業",
    "規制・政策",
    "オープンソース",
    "その他",
]
