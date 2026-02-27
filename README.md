# AI News Daily 🤖📰

AI分野の最新ニュースを毎日自動収集・要約してWebサイトに掲載するシステムです。

## 🔧 セットアップ手順

### 1. 前提条件

- **Googleアカウント**（Gemini APIキー取得に必要）
- **GitHubアカウント**（ホスティング＆自動実行に必要）
- **Python 3.10以上**（ローカル実行時）

### 2. Gemini APIキーの取得

1. [Google AI Studio](https://aistudio.google.com/apikey) にアクセス
2. Googleアカウントでログイン
3. 「APIキーを作成」をクリック
4. 生成されたAPIキーをコピーして安全な場所に保管

### 3. GitHubリポジトリの作成

1. このフォルダをGitリポジトリとして初期化:
   ```bash
   cd ai-news-site
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. GitHubで新しいリポジトリを作成（公開リポジトリ推奨）

3. リモートリポジトリに接続してプッシュ:
   ```bash
   git remote add origin https://github.com/あなたのユーザー名/ai-news-site.git
   git branch -M main
   git push -u origin main
   ```

### 4. GitHub Secretsの設定

1. GitHubリポジトリのページで **Settings** → **Secrets and variables** → **Actions** を開く
2. **New repository secret** をクリック
3. 以下を入力:
   - **Name**: `GEMINI_API_KEY`
   - **Secret**: 手順2で取得したAPIキー
4. **Add secret** をクリック

### 5. GitHub Pagesの有効化

1. GitHubリポジトリの **Settings** → **Pages** を開く
2. **Source**: `Deploy from a branch` を選択
3. **Branch**: `main` / `docs` を選択
4. **Save** をクリック
5. 数分後に `https://あなたのユーザー名.github.io/ai-news-site/` でサイトが公開される

### 6. 動作確認

1. リポジトリの **Actions** タブを開く
2. **AI News Daily Update** ワークフローを選択
3. **Run workflow** → **Run workflow** をクリック
4. 実行完了後、GitHub Pagesのサイトを確認

## 🖥️ ローカル実行

```bash
# 依存パッケージのインストール
pip install -r scripts/requirements.txt

# 環境変数の設定
set GEMINI_API_KEY=あなたのAPIキー

# ニュース取得＆要約＆サイト生成
python scripts/main.py
```

生成されたサイトは `docs/index.html` をブラウザで開いて確認できます。

## 📁 ファイル構成

```
ai-news-site/
├── .github/workflows/
│   └── daily-news.yml      # GitHub Actions（毎日自動実行）
├── scripts/
│   ├── config.py            # 設定
│   ├── fetch_news.py        # ニュース収集
│   ├── summarize.py         # Gemini API要約
│   ├── generate_site.py     # HTMLサイト生成
│   ├── main.py              # メインスクリプト
│   └── requirements.txt     # Python依存パッケージ
├── docs/                    # GitHub Pages公開ディレクトリ
│   ├── index.html           # メインページ
│   ├── style.css            # スタイル
│   ├── script.js            # フロントエンドJS
│   └── data/                # ニュースデータ（JSON）
├── templates/
│   └── index.html           # HTMLテンプレート
└── README.md
```

## ⚙️ カスタマイズ

### ニュースソースの追加・変更

`scripts/config.py` の `RSS_FEEDS` リストを編集：

```python
RSS_FEEDS = [
    {
        "name": "ソース名",
        "url": "https://example.com/rss",
        "language": "ja",  # または "en"
    },
    # ...
]
```

### 取得件数の調整

`scripts/config.py` の以下の値を変更：

```python
MAX_ARTICLES_PER_FEED = 5   # 1フィードあたりの最大記事数
MAX_TOTAL_ARTICLES = 25      # 合計最大記事数
HOURS_LOOKBACK = 48          # 過去何時間の記事を取得するか
```

### 実行スケジュールの変更

`.github/workflows/daily-news.yml` のcron式を変更：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 0:00 (JST 9:00)
```

## 💰 コスト

| 項目 | コスト |
|------|--------|
| Gemini API | 無料 |
| GitHub Pages | 無料 |
| GitHub Actions | 無料（月2000分まで） |
| **合計** | **完全無料** |
