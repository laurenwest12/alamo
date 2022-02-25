from config import URL, sid, auth_token, twilio_number, text_numbers, movie_to_search

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from twilio.rest import Client


s = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=s, options=options)

wait = WebDriverWait(driver, 10)


def get_movie_names():
    movies_elements = driver.find_elements(By.TAG_NAME, 'alamo-card-title')
    movies = []

    for movie in movies_elements:
        movies.append(movie.text)

    return movies


def find_if_movie_is_out(movies, search_movie):
    movie_out = False
    movie_out_name = ''

    for current_movies in movies:
        if search_movie.lower() in current_movies.lower():
            movie_out = True
            movie_out_name = current_movies

    return {
        "movie_out": movie_out,
        "movie_out_name": movie_out_name
    }


def send_text(movie):
    for number in text_numbers:
        client = Client(sid, auth_token)
        client.messages.create(
            to=number,
            from_=twilio_number,
            body=f"Movie {movie} is available to buy tickets at Alamo"
        )


def text_if_movie_out(url):
    driver.get(url)
    time.sleep(1)
    movies = get_movie_names()
    movie_out = find_if_movie_is_out(movies, movie_to_search)

    if movie_out["movie_out"] == True:
        send_text(movie_out["movie_out_name"])

    driver.close()


text_if_movie_out(URL)
