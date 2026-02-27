/**
 * AI News Daily - フロントエンドJavaScript
 * カテゴリフィルタ・日付切替のインタラクション
 */

document.addEventListener('DOMContentLoaded', () => {
    initCategoryFilter();
    initDateSelector();
});

/**
 * カテゴリフィルタの初期化
 */
function initCategoryFilter() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const newsCards = document.querySelectorAll('.news-card');

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // アクティブボタン更新
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const selectedCategory = btn.dataset.category;

            // カード表示切替
            let visibleCount = 0;
            newsCards.forEach((card, index) => {
                if (selectedCategory === 'all' || card.dataset.category === selectedCategory) {
                    card.classList.remove('hidden');
                    card.style.animationDelay = `${visibleCount * 0.05}s`;
                    card.style.animation = 'none';
                    // reflow
                    card.offsetHeight;
                    card.style.animation = '';
                    visibleCount++;
                } else {
                    card.classList.add('hidden');
                }
            });

            // 件数更新
            updateArticleCount(visibleCount);
        });
    });
}

/**
 * 日付セレクタの初期化
 */
function initDateSelector() {
    const dateSelect = document.getElementById('date-select');
    if (!dateSelect) return;

    dateSelect.addEventListener('change', async (e) => {
        const selectedDate = e.target.value;
        await loadNewsData(selectedDate);
    });
}

/**
 * 指定日付のニュースデータを読み込み
 */
async function loadNewsData(dateStr) {
    const grid = document.getElementById('news-grid');
    if (!grid) return;

    // ローディング表示
    grid.innerHTML = `
        <div class="loading active">
            <div class="loading-spinner"></div>
            <p style="color: var(--text-secondary);">ニュースを読み込み中...</p>
        </div>
    `;

    try {
        const response = await fetch(`data/news_${dateStr}.json`);
        if (!response.ok) {
            throw new Error(`データが見つかりません: ${dateStr}`);
        }

        const data = await response.json();
        renderNewsCards(data.articles, data.count);

        // フィルタをリセット
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(b => b.classList.remove('active'));
        const allBtn = document.getElementById('filter-all');
        if (allBtn) allBtn.classList.add('active');

    } catch (error) {
        grid.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <h2>データが見つかりません</h2>
                <p>${dateStr}のニュースデータはまだ収集されていません。</p>
            </div>
        `;
    }
}

/**
 * ニュースカードをレンダリング
 */
function renderNewsCards(articles, count) {
    const grid = document.getElementById('news-grid');
    if (!grid) return;

    if (!articles || articles.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <h2>ニュースがありません</h2>
                <p>この日のニュースデータは空です。</p>
            </div>
        `;
        updateArticleCount(0);
        return;
    }

    // カテゴリ→カラーインデックスのマッピング
    const categoryColors = {};
    let colorIndex = 0;

    grid.innerHTML = articles.map((article, idx) => {
        if (!(article.category in categoryColors)) {
            categoryColors[article.category] = colorIndex % 6;
            colorIndex++;
        }
        const catColor = categoryColors[article.category];
        const publishedDate = article.published ? article.published.substring(0, 10) : '';

        return `
            <article class="news-card" data-category="${escapeHtml(article.category)}" id="card-${escapeHtml(article.id)}" style="animation-delay: ${idx * 0.05}s">
                <div class="card-header">
                    <span class="card-category cat-${catColor}">${escapeHtml(article.category)}</span>
                    <span class="card-source">${escapeHtml(article.source)}</span>
                </div>
                <h2 class="card-title">
                    <a href="${escapeHtml(article.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(article.title)}</a>
                </h2>
                <p class="card-summary">${escapeHtml(article.summary)}</p>
                <div class="card-footer">
                    <time class="card-date" datetime="${escapeHtml(article.published)}">${publishedDate}</time>
                    <a href="${escapeHtml(article.url)}" target="_blank" rel="noopener noreferrer" class="card-link">
                        記事を読む →
                    </a>
                </div>
            </article>
        `;
    }).join('');

    updateArticleCount(articles.length);

    // カテゴリフィルタを再接続
    initCategoryFilter();
}

/**
 * 記事件数を更新
 */
function updateArticleCount(count) {
    const badge = document.getElementById('article-count');
    if (badge) {
        badge.textContent = `📰 ${count}件の記事`;
    }
}

/**
 * HTMLエスケープ
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}
