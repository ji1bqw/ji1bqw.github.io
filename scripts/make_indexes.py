from bs4 import BeautifulSoup
import os
import glob
from collections import defaultdict
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
    parts = rel.split(os.sep)
    articles.append({'title': title, 'date_str': date_str, 'sort_key': sort_key,
                     'rel': rel, 'year': parts[0], 'month': parts[1]})

articles.sort(key=lambda a: a['sort_key'], reverse=True)

STYLE = """
<style>
body { font-family: sans-serif; max-width: 860px; margin: 0 auto; padding: 1em; }
h1 { font-size: 1.5em; border-bottom: 2px solid #444; }
ul { list-style: none; padding: 0; }
li { padding: 0.3em 0; border-bottom: 1px solid #eee; }
.date { color: #888; font-size: 0.85em; margin-right: 0.5em; }
.month-list li { display: inline-block; margin: 0.3em; }
.month-list a { display: inline-block; padding: 0.2em 0.7em; background: #f0f0f0; border-radius: 3px; text-decoration: none; color: #333; }
.month-list a:hover { background: #ddd; }
footer { margin-top: 2em; border-top: 1px solid #ccc; font-size: 0.8em; color: #666; }
</style>
"""

# 月別index
by_ym = defaultdict(list)
by_year = defaultdict(list)
for a in articles:
    by_ym[(a['year'], a['month'])].append(a)
    by_year[a['year']].append(a)

for (year, month), arts in by_ym.items():
    arts.sort(key=lambda a: a['sort_key'], reverse=True)
    items = ''.join(f'<li><span class="date">{a["date_str"]}</span> <a href="{os.path.basename(a["rel"])}">{a["title"]}</a></li>\n' for a in arts)
    body = f'<h1>{year}年{month}月の記事</h1>\n<ul>{items}</ul>'
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{year}年{month}月 - JI1BQW CyberHAM</title>
<link rel="stylesheet" href="../../styles.css" type="text/css" />
{STYLE}
</head>
<body>
<p><a href="../../index.html">← トップページへ</a></p>
{body}
<footer><p>JI1BQW CyberHAM | <a href="../../index.html">トップページ</a></p></footer>
</body>
</html>"""
    path = os.path.join(src_base, year, month, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

# 年別index
for year, arts in by_year.items():
    months = sorted(set(a['month'] for a in arts), reverse=True)
    month_links = ''.join(f'<li><a href="{m}/index.html">{year}年{m}月</a></li>\n' for m in months)
    body = f'<h1>{year}年の記事</h1>\n<ul class="month-list">{month_links}</ul>'
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{year}年 - JI1BQW CyberHAM</title>
<link rel="stylesheet" href="../styles.css" type="text/css" />
{STYLE}
</head>
<body>
<p><a href="../index.html">← トップページへ</a></p>
{body}
<footer><p>JI1BQW CyberHAM | <a href="../index.html">トップページ</a></p></footer>
</body>
</html>"""
    path = os.path.join(src_base, year, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

print(f'月別index: {len(by_ym)}件')
print(f'年別index: {len(by_year)}件')
