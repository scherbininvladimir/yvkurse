import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

import settings


class CompareSource(object):
    def __init__(self, source):
        self.previous_source = source


    def __call__(self, driver):
        if self.previous_source != driver.page_source:
            return True
        else:
            return False


def login_vk():
    url = 'https://vk.com/login'
    driver.get(url)
    driver.find_element_by_id("email").send_keys(settings.login)
    driver.find_element_by_id("pass").send_keys(settings.password)
    driver.find_element_by_id("login_button").click()
    source = driver.page_source
    WebDriverWait(driver, 20).until(CompareSource(source))


def get_article_blocks():
    def get_more():
        source = driver.page_source
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            try:
                WebDriverWait(driver, 5).until(CompareSource(source))
                source = driver.page_source
            except TimeoutException:
                break

    
    driver.get(settings.url)
    get_more()


def get_csv_content(links):
    csv_content = ""
    for link in links:
        r = requests.get(link)
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
        print(article_title)
        csv_content = csv_content + f"'{article_title}', '{article_text}', '{article_images}';\n"
    return csv_content


options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
# driver = webdriver.Chrome(executable_path='./chromedriver')
login_vk()
driver.get(settings.url)
get_article_blocks()
soup = BeautifulSoup(driver.page_source, "html.parser")
article_blocks = soup.find_all("div", class_="author_page_block")
article_blocks = article_blocks + soup.find_all("div", class_="author_page_grid_article")
article_links = ["https://vk.com/" + article_block.find("a")["href"].split("/")[1] for article_block in article_blocks]
driver.close()
with open(settings.output_file, "w", encoding="utf-8") as file:
    print("'title', 'text', 'images';", file=file)
    print(get_csv_content(article_links), file=file)
print(f'Загружено статей: {len(article_links)}')
