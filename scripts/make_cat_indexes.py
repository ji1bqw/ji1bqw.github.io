from bs4 import BeautifulSoup
import os
import glob
from collections import defaultdict

src_orig = os.path.expanduser('~/Common/Hamradio/Nifty Blog backup/cyberham')
src_base = os.path.expanduser('~/github/ji1bqw.github.io')

cat_names = {
    'dstar': 'D-STAR',
    'echoirlp': 'EchoIRLP',
    'dextra': 'DEXTRA',
    'asterisk_app_rpt': 'Asterisk/app_rpt',
    'rtpdir': 'rtpDir',
    'cat24376443': 'VARA/VarAC',
    'cat6856981': 'IRLP構築日記',
    'cat6858662': 'IRLP #8437 ノード情報',
    'cat21348361': '備忘録',
    'off_the_topic': 'アマチュア無線一般',
    'cat6857067': 'お知らせ',
}

cat_articles = defaultdict(list)
html_files = glob.glob(os.path.join(src_orig, '[0-9][0-9][0-9][0-9]', '[0-9][0-9]', '*.html'))
html_files = [f for f in html_files if 'no_prefetch' not in f and 'index.html' not in f]

for src_path in html_files:
    with open(src_path, encoding='utf-8', errors='replace') as f:
        soup = BeautifulSoup(f, 'html.parser')
    footer = soup.find('span', class_='post-footers')
    if not footer:
        continue
    cat_link = footer.find('a')
    if not cat_link:
        continue
    href = cat_link.get('href', '')
    cat_key = href.split('/')[-2] if '/' in href else ''
    if cat_key not in cat_names:
        continue
    h3 = soup.find('h3')
    title = h3.get_text(strip=True) if h3 else '無題'
    # ファイルパスから年月日を取得してソートキーに使用
    rel = os.path.relpath(src_path, src_orig)
    parts = rel.split(os.sep)
    year, month = parts[0], parts[1]
    # post-footers から日付文字列を取得
    footer_text = footer.get_text()
    import re
    m = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', footer_text)
    if m:
        sort_key = f"{m.group(1)}{int(m.group(2)):02d}{int(m.group(3)):02d}"
        date_str = f"{m.group(1)}年{m.group(2)}月{m.group(3)}日"
    else:
        sort_key = f"{year}{month}00"
        date_str = f"{year}年{month}月"
    cat_articles[cat_key].append({'title': title, 'date_str': date_str, 'sort_key': sort_key, 'rel': rel})

STYLE = """
<style>
body { font-family: sans-serif; max-width: 860px; margin: 0 auto; padding: 1em; }
h1 { font-size: 1.5em; border-bottom: 2px solid #444; }
ul { list-style: none; padding: 0; }
li { padding: 0.3em 0; border-bottom: 1px solid #eee; }
.date { color: #888; font-size: 0.85em; margin-right: 0.5em; }
footer { margin-top: 2em; border-top: 1px solid #ccc; font-size: 0.8em; color: #666; }
</style>
"""

for cat_key, arts in cat_articles.items():
    arts.sort(key=lambda a: a['sort_key'], reverse=True)
    items = ''
    for a in arts:
        rel_from_cat = '../' + a['rel'].replace(os.sep, '/')
        items += f'<li><span class="date">{a["date_str"]}</span> <a href="{rel_from_cat}">{a["title"]}</a></li>\n'
    cat_name = cat_names[cat_key]
    body = f'<h1>{cat_name}</h1>\n<ul>{items}</ul>'
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cat_name} - JI1BQW CyberHAM</title>
<link rel="stylesheet" href="../styles.css" type="text/css" />
{STYLE}
</head>
<body>
<p><a href="../index.html">← トップページへ</a></p>
{body}
<footer><p>JI1BQW CyberHAM | <a href="../index.html">トップページ</a></p></footer>
</body>
</html>"""
    path = os.path.join(src_base, cat_key, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{cat_name}: {len(arts)}記事')

print('完了')
