import requests
import threading
import time
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from config import API_KEY
import uuid
import os

es=Elasticsearch("http://localhost:9200/")
client=MongoClient("mongodb://localhost:27017")
db=client['news_db']
users_collection=db['articles']


def scrape_articles():
    url = f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={API_KEY}&pageSize=20"
    page = 1  # Start from page 1

    while True:
        paginated_url = f"{url}&page={page}"
        response = requests.get(paginated_url)

        if response.status_code == 200:
            articles = response.json().get('articles', [])
            if not articles:
                print("No more articles found.")
                break

            for article in articles:
                title = article.get('title', '')
                author = article.get('author', '')
                content = article.get('content', '')
                existing_article = db['articles'].find_one(
                    {"title": article['title'], "author": article['author']})

                if existing_article:
                    return  # Skip indexing if duplicate is found
                db['articles'].insert_one({
                    'title': title,
                    'author': author,
                    'content': content
                })
                unique_id = str(uuid.uuid4())
                es.index(index="documents", id=unique_id, body={
                    'title': title,
                    'author': author,
                    'content': content
                })

                print(f"Saved Article: {title}")

            page += 1
        else:
            print(f"Failed to retrieve articles. Status code: {response.status_code}")

        time.sleep(600)


def background_task():
    thread = threading.Thread(target=scrape_articles)
    thread.daemon = True
    thread.start()


background_task()
