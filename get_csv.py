import requests
from bs4 import BeautifulSoup

import settings


def get_csv_string(link):
    site = settings.url.split('@')[0]
    r = requests.get(site + link)
    soup = BeautifulSoup(r.text, "html.parser")
    article_block = soup.find("div", class_="article_view")
    article_title = ""
    article_text = ""
    article_images = ""
    if article_block:
        article_title = article_block.find("h1").text.strip()
        text_blocks = [p for p in article_block.find_all("p")]
        for paragraph in text_blocks:
            article_text = article_text + paragraph.getText()
        images = [image.get("src") for image in article_block.find_all("img")]
        for image in images:
            if article_images:
                article_images = article_images + ", "
            article_images = article_images + image
    return f"'{article_title}', '{article_text}', '{article_images}';"


r = requests.get(settings.url, headers=settings.headers)
soup = BeautifulSoup(r.text, "html.parser")
main_article_block = soup.find("div", class_="author_page_block")
main_article_block_link = ""
if main_article_block:
    main_article_block_link = main_article_block.find('a').get('href')
article_links = [link.find("a").get("href") for link in soup.find_all("div", class_="author_page_grid_article")]

with open(settings.output_file, "w", encoding="utf-8") as file:
    if main_article_block_link:
        print("'title', 'text', 'images'", file=file, sep="\n")
        print(get_csv_string(main_article_block_link), file=file, sep="\n")
        for link in article_links:
            print(get_csv_string(link), file=file, sep="\n")
        print(f'Статьи выгружены в {settings.output_file}')
    else:
        print("Статьи не найдены")
