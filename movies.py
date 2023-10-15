import os
import requests
import numpy as np
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def load_movies():
    headers = {"X-API-KEY": os.getenv("X-API-KEY")}

    for page in range(1, 227):
        params = {"rating.kp": "6-8",
                  'selectFields': ["name", "rating.kp", "rating.imdb",
                                   "year", "countries.name"],
                  "page": page}
        response = requests.get(
            "https://api.kinopoisk.dev/v1.3/movie?limit=250",
            headers=headers,
            params=params)

    return response.json()


def calculate_rating_difference(movies):
    kp_ratings = []
    imdb_ratings = []
    for movie in movies["docs"]:
        kp_rating = movie["rating"]["kp"]
        imdb_rating = movie["rating"]["imdb"]

        kp_ratings.append(kp_rating)
        imdb_ratings.append(imdb_rating)

    kp_mean = np.mean(kp_ratings)
    imdb_mean = np.mean(imdb_ratings)

    return round(kp_mean - imdb_mean, 2)


def calculate_most_successful_year(movies):
    years = [movie["year"] for movie in movies["docs"]]
    unique_years, counts = np.unique(years, return_counts=True)

    most_successful_year = unique_years[np.argmax(counts)]

    return most_successful_year


def calculate_most_successful_country(movies):
    countries = [movie["countries"][0] for movie in movies["docs"]
                 if movie["countries"]]
    countries_all = []
    for i in range(len(countries)):
        for key, value in countries[i].items():
            countries_all.append(value)
    unique_countries, counts = np.unique(countries_all, return_counts=True)

    most_successful_country = unique_countries[np.argmax(counts)]

    return most_successful_country


def save_movies(movies):
    conn = psycopg2.connect(database=os.getenv("POSTGRES_DB", "moviesdb"),
                            user=os.getenv("POSTGRES_USER", "postgres"),
                            password=os.getenv("POSTGRES_PASSWORD", ""))
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS movies (title TEXT, year INTEGER, kp_rating REAL, imdb_rating REAL, country TEXT)")

    for movie in movies["docs"]:
        title = movie["name"]
        year = movie["year"]
        kp_rating = movie["rating"]["kp"]
        imdb_rating = movie["rating"]["imdb"]
        country = ", ".join([country["name"] for country in movie["countries"]])

        cursor.execute("INSERT INTO movies (title, year, kp_rating, imdb_rating, country) VALUES (%s, %s, %s, %s, %s)",
                       (title, year, kp_rating, imdb_rating, country))

    conn.commit()
    conn.close()


def main():
    movies = load_movies()

    average_difference = calculate_rating_difference(movies)
    most_successful_year = calculate_most_successful_year(movies)
    most_successful_country = calculate_most_successful_country(movies)

    print("Среднее расхождение оценки от платформы IMBD и Кинопоиск:", average_difference)
    print("Самый успешный год кинопроизводства с точки зрения оценок:", most_successful_year)
    print("Самая успешная страна с точки зрения оценок:", most_successful_country)

    save_movies(movies)
    


if __name__ == "__main__":
    main()
