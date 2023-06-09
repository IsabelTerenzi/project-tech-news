import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        response = requests.get(url, headers={"user-agent": "Fake user-agent"})
        time.sleep(1)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    response = Selector(html_content)
    return response.css(".cs-overlay-link::attr(href)").getall()


# Requisito 3
def scrape_next_page_link(html_content):
    response = Selector(html_content)
    return response.css(".next.page-numbers::attr(href)").get()


# Requisito 4
def scrape_news(html_content):
    response = Selector(html_content)

    url = response.css("link[rel=canonical]::attr(href)").get()
    title = response.css(".entry-title::text").get()
    timestamp = response.css(".meta-date::text").get()
    writer = response.css(".author a ::text").get()
    reading_time = response.css(".meta-reading-time::text").re_first(r"\d+")
    summary = response.css(".entry-content > p:first-of-type *::text").getall()
    category = response.css(".meta-category span.label::text").get()

    noticia = {
        "url": url,
        "title": title.strip(),
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": int(reading_time),
        "summary": "".join(summary).strip(),
        "category": category,
    }

    return noticia


# Requisito 5
def get_tech_news(amount):
    noticias = []
    url_blog = "https://blog.betrybe.com"
    contador = 0

    while contador < amount:
        get_blog_trybe = fetch(url_blog)
        get_all_pages = scrape_updates(get_blog_trybe)

        for page in get_all_pages:
            get_blog_page = fetch(page)
            noticias.append(scrape_news(get_blog_page))
            contador += 1

            if (contador == amount):
                break

        url_blog = scrape_next_page_link(get_blog_trybe)

    create_news(noticias)

    return noticias
