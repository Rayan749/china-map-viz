import pathlib
import shutil

from bs4 import BeautifulSoup


def ads(index_path):
    adsense_url = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"
    GA_AdSense = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4914616940850872"
     crossorigin="anonymous"></script>"""

    # Insert the script in the head tag of the static template inside your virtual

    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find(GA_AdSense, src=adsense_url):
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)
        else:
            shutil.copy(index_path, bck_index)
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + GA_AdSense)
        index_path.write_text(new_html)
