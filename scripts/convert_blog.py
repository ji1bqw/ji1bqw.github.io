import os
import glob
import shutil
from bs4 import BeautifulSoup

src_base = os.path.expanduser("~/Common/Hamradio/Nifty Blog backup/cyberham")
dst_base = os.path.expanduser("~/github/ji1bqw.github.io")

converted = 0
skipped = 0

html_files = glob.glob(os.path.join(src_base, "**", "*.html"), recursive=True)
html_files = [f for f in html_files if "no_prefetch" not in f]

for src_path in html_files:
    rel_path = os.path.relpath(src_path, src_base)
    dst_path = os.path.join(dst_base, rel_path)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    with open(src_path, encoding="utf-8", errors="replace") as f:
        soup = BeautifulSoup(f, "html.parser")

    body_div = soup.find("div", class_="entry-body-text")
    if not body_div:
        shutil.copy2(src_path, dst_path)
        skipped += 1
        continue

    h3 = soup.find("h3")
    title = h3.get_text(strip=True) if h3 else "無題"
    h2 = soup.find("h2")
    date = h2.get_text(strip=True) if h2 else ""
    nav = soup.find_all("div", class_="entry-nav")
    prev_next = str(nav[0]) if nav else ""
    prev_next = prev_next.replace("?no_prefetch=1", "")

    depth = len(rel_path.split(os.sep)) - 1
    root = "../" * depth if depth > 0 else "./"
    css_path = root + "styles.css"
    top_path = root + "index.html"

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - JI1BQW CyberHAM</title>
<link rel="stylesheet" href="{css_path}" type="text/css" />
<style>
body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 1em; }}
h1 {{ font-size: 1.4em; border-bottom: 2px solid #666; }}
.date {{ color: #666; font-size: 0.9em; }}
.entry-body {{ margin: 1em 0; line-height: 1.8; }}
.entry-nav {{ margin: 1em 0; font-size: 0.9em; }}
footer {{ margin-top: 2em; border-top: 1px solid #ccc; font-size: 0.8em; color: #666; }}
</style>
</head>
<body>
<p><a href="{top_path}">&#8592; トップページへ</a></p>
<h1>{title}</h1>
<p class="date">{date}</p>
<div class="entry-body">
{body_div}
</div>
{prev_next}
<footer>
<p>JI1BQW CyberHAM | <a href="{top_path}">トップページ</a></p>
</footer>
</body>
</html>
"""

    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(html)
    converted += 1

for item in ["styles.css", "images", "qrcode.png", "atom.xml", "rss.xml", "index.rdf"]:
    src = os.path.join(src_base, item)
    dst = os.path.join(dst_base, item)
    if os.path.isdir(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    elif os.path.isfile(src):
        shutil.copy2(src, dst)

print(f"変換完了: {converted}記事")
print(f"そのままコピー: {skipped}ファイル")
