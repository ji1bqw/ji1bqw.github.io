from bs4 import BeautifulSoup
import os
import glob
import re

src_orig = os.path.expanduser('~/Common/Hamradio/Nifty Blog backup/cyberham')
src_base = os.path.expanduser('~/github/ji1bqw.github.io')

articles = []
html_files = glob.glob(os.path.join(src_orig, '[0-9][0-9][0-9][0-9]', '[0-9][0-9]', '*.html'))
html_files = [f for f in html_files if 'no_prefetch' not in f and 'index.html' not in f]

for src_path in html_files:
    with open(src_path, encoding='utf-8', errors='replace') as f:
        soup = BeautifulSoup(f, 'html.parser')
    h3 = soup.find('h3')
    if not h3:
        continue
    title = h3.get_text(strip=True)
    footer = soup.find('span', class_='post-footers')
    m = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', footer.get_text() if footer else '')
    if m:
        sort_key = f"{m.group(1)}{int(m.group(2)):02d}{int(m.group(3)):02d}"
        date_str = f"{m.group(1)}年{m.group(2)}月{m.group(3)}日"
    else:
        rel = os.path.relpath(src_path, src_orig)
        parts = rel.split(os.sep)
        sort_key = f"{parts[0]}{parts[1]}00"
        date_str = f"{parts[0]}年{parts[1]}月"
    rel = os.path.relpath(src_path, src_orig)
    articles.append({'title': title, 'date_str': date_str, 'sort_key': sort_key, 'rel': rel})

articles.sort(key=lambda a: a['sort_key'], reverse=True)
latest = articles[:15]

latest_html = ''
for a in latest:
    latest_html += f'<li><span class="date">{a["date_str"]}</span> <a href="{a["rel"].replace(os.sep, "/")}">{a["title"]}</a></li>\n'

years = sorted(set(a['rel'].split(os.sep)[0] for a in articles), reverse=True)
years_html = ''.join(f'<li><a href="{y}/index.html">{y}年</a></li>\n' for y in years)

index_html = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JI1BQW CyberHAM</title>
<link rel="stylesheet" href="styles.css" type="text/css" />
<style>
body { font-family: sans-serif; max-width: 860px; margin: 0 auto; padding: 1em; }
h1 { font-size: 1.8em; border-bottom: 3px solid #444; margin-bottom: 0.2em; }
h2 { font-size: 1.2em; border-left: 4px solid #666; padding-left: 0.5em; margin-top: 1.5em; }
.subtitle { color: #666; margin-bottom: 1.5em; }
ul { list-style: none; padding: 0; }
li { padding: 0.3em 0; border-bottom: 1px solid #eee; }
.date { color: #888; font-size: 0.85em; margin-right: 0.5em; }
.cat-list li, .year-list li { display: inline-block; margin: 0.3em; }
.cat-list a, .year-list a { display: inline-block; padding: 0.2em 0.7em; background: #f0f0f0; border-radius: 3px; text-decoration: none; color: #333; }
.cat-list a:hover, .year-list a:hover { background: #ddd; }
footer { margin-top: 2em; border-top: 1px solid #ccc; font-size: 0.8em; color: #666; padding-top: 0.5em; }
</style>
</head>
<body>
<h1>JI1BQW CyberHAM</h1>
<p class="subtitle">--- Internet Linked Radio Amateur --- アマチュア無線関連ブログアーカイブ (2007-2023)</p>

<h2>カテゴリ</h2>
<ul class="cat-list">
<li><a href="dstar/index.html">D-STAR</a></li>
<li><a href="echoirlp/index.html">EchoIRLP</a></li>
<li><a href="dextra/index.html">DEXTRA</a></li>
<li><a href="asterisk_app_rpt/index.html">Asterisk/app_rpt</a></li>
<li><a href="rtpdir/index.html">rtpDir</a></li>
<li><a href="cat24376443/index.html">VARA/VarAC</a></li>
<li><a href="cat6856981/index.html">IRLP構築日記</a></li>
<li><a href="cat6858662/index.html">IRLP #8437 ノード情報</a></li>
<li><a href="cat21348361/index.html">備忘録</a></li>
<li><a href="off_the_topic/index.html">アマチュア無線一般</a></li>
<li><a href="cat6857067/index.html">お知らせ</a></li>
</ul>

<h2>バックナンバー</h2>
<ul class="year-list">
""" + years_html + """</ul>

<h2>最新記事</h2>
<ul>
""" + latest_html + """</ul>

<footer>
<p>JI1BQW CyberHAM | アマチュア無線局 JI1BQW のブログアーカイブ</p>
</footer>
</body>
</html>
"""

with open(os.path.join(src_base, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)

print(f'完了 総記事数: {len(articles)}')
