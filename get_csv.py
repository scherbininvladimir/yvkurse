import re
import requests
from bs4 import BeautifulSoup

import settings


def get_csv_string(link, file):
    site = settings.url.split('@')[0]
    r = requests.get(site + link)
    soup = BeautifulSoup(r.text, "html.parser")
    article_block = soup.find("div", class_="article_view")
    article_title = ""
    article_text = ""
    article_images = ""
    if article_block:
        if article_block.find("h1"):
            article_title = article_block.find("h1").text.strip()
        text_blocks = [p for p in article_block.find_all("p")]
        for paragraph in text_blocks:
            article_text = article_text + paragraph.getText()
        images = [image.get("src") for image in article_block.find_all("img")]
        for image in images:
            if article_images:
                article_images = article_images + ", "
            article_images = article_images + image
    print(f"'{article_title}', '{article_text}', '{article_images}';", file=file, sep="\n")
    for script in soup.find_all("script"):
        if re.match(r'.*"next_article_url":"\\(.*)"', str(script)):
            next_link = re.match(r'.*"next_article_url":"\\(.*)"', str(script)).group(1)
            get_csv_string(next_link, file)    
    return

r = requests.get(settings.url)

soup = BeautifulSoup(r.text, "html.parser")
main_article_block = soup.find("div", class_="author-page-article")
main_article_block_link = ""
if main_article_block:
    main_article_block_link = main_article_block.find('a').get('href')

with open(settings.output_file, "w", encoding="utf-8") as file:
    print("'title', 'text', 'images'", file=file, sep="\n")
    get_csv_string(main_article_block_link, file)
