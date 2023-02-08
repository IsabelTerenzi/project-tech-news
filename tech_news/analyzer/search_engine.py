from tech_news.database import search_news
import datetime


# Requisito 7
def search_by_title(title):
    noticia = search_news({"title": {"$regex": title, "$options": "i"}})
    noticias = [(news["title"], news["url"]) for news in noticia]

    return noticias


# Requisito 8
def search_by_date(date):
    try:
        data_formatada = datetime.date.fromisoformat(date).strftime("%d/%m/%Y")
        noticia = search_news({"timestamp": data_formatada})
        noticias = [(news["title"], news["url"]) for news in noticia]
    except ValueError:
        raise ValueError('Data inválida')

    return noticias

# https://medium.com/data-hackers/como-manipular-datetime-no-python-578f07b72920


# Requisito 9
def search_by_category(category):
    noticia = search_news({"category": {"$regex": category, "$options": "i"}})
    noticias = [(news["title"], news["url"]) for news in noticia]

    return noticias
