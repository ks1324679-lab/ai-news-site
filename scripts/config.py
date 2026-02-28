"""
設定ファイル - AIニュース自動収集システム
"""
import os

# Gemini API設定
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-1.5-flash"

# RSSフィード一覧（AI分野）
RSS_FEEDS = [
    # --- 生成AI関連ソース ---
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
]

# 取得設定
MAX_ARTICLES_PER_FEED = 5  # 1フィードあたりの最大記事数
MAX_TOTAL_ARTICLES = 30     # 合計最大記事数
HOURS_LOOKBACK = 48         # 過去何時間の記事を取得するか

# ファイルパス
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
DATA_DIR = DOCS_DIR / "data"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# カテゴリ一覧（生成AIをトップに配置）
CATEGORIES = [
    "生成AI",
    "研究・論文",
    "プロダクト・サービス",
    "ビジネス・企業",
    "規制・政策",
    "オープンソース",
    "その他",
]
