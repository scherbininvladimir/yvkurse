import requests
from bs4 import BeautifulSoup

import settings

def get_csv_string(link):
    site = settings.url.split('@')[0]
    r = requests.get(site + link, headers=settings.headers)
    soup = BeautifulSoup(r.text, "html.parser")
    article_block = soup.find("div", class_="article_view")
    article_title = ""
    article_text = ""
    article_images = ""
    if article_block:
        article_title = article_block.find("h1").text.strip()
        images = [image.get("src") for image in article_block.find_all("img")]
        text_blocks = [p for p in article_block.find_all("p")]
    
        for paragraph in text_blocks:
            article_text = article_text + paragraph.getText()
    
        for image in images:
            if article_images:
                article_images = article_images + ", "
            article_images = article_images + image
    return f"'{article_title}', '{article_text}', '{article_images}';"


r = requests.get(settings.url, headers=settings.headers)
soup = BeautifulSoup(r.text, "html.parser")
block_main_article_link = soup.find("div", class_="author_page_block_main_article").find('a').get('href')
article_links = [link.find("a").get("href") for link in soup.find_all("div", class_="author_page_grid_article")]

with open(settings.output_file, "w") as file:
    print(get_csv_string(block_main_article_link), file=file, sep="\n")
    for link in article_links:
        print(get_csv_string(link), file=file, sep="\n")
        
   


