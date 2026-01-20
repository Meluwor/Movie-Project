import os
import socket

import requests
from dotenv import load_dotenv

BASE_URL = "http://www.omdbapi.com"

# im not sure if this is the way to go because im changing/setting it later/at start.
API_KEY = None


# INFO  I tried with header but cant get any results also just found comments in net that also says it need to be send inside the url
# headers = {
# "apikey": API_KEY
# }
# just unauthorized

def set_api_key(key):
    """
    This function sets the API-Key at the very start of the program
    """
    global API_KEY
    API_KEY = key


def get_api_key():
    """
    This function will get the API-Key from the .env file.
    It will return NONE if there isn't an API-Key inside this file.
    """
    load_dotenv()
    return os.getenv('API_KEY')


def is_internet_available():
    """
    A simple check if there is an internet connection.
    """
    try:
        # the ip to google.com lets hope they will stay for a while
        ip = "8.8.8.8"
        # DNS port
        port = 53
        socket.create_connection((ip, port), timeout=3)
        return True
    except OSError:
        return False


def is_api_available():
    """
    A simple check if the OMDB-Api is available
    """
    try:
        # using requests.head to get minimal data from the website
        response = requests.head(BASE_URL, timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False


def is_api_key_valid():
    """
    A simple check if the API-Key is valid
    """
    # The API returns this if the key is not valid   {"Response": "False","Error": "Invalid API key!"}
    # The status code is 401 in that case

    params = {
        "apikey": API_KEY,
        "t": "The Matrix"  # could be any other available movie title
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        # this shall ensure a more stable request
        response.raise_for_status()
        movie_data = response.json()
        return movie_data.get("Response") == "True"

    except requests.RequestException as e:
        return False


def get_movie_by_name(movie_name):
    """
    This function shall get a movie from the API by given movie name.
    """
    # if the movie wasn't found {"Response": "False","Error": "Movie not found!"}

    params = {
        "apikey": API_KEY,
        "t": movie_name  # t is the parameter for searching a movie by title
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        # this shall ensure a more stable request
        response.raise_for_status()
        movie_data = response.json()
        if movie_data.get("Response") == "True":
            return movie_data
        else:
            return {}
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return {}


def search_movie(movie_name):
    """
    This function shall get a movie from the API by given movie name.
    Beware of the following: The movie data will not contain a rating just the rating ID
    """
    # if the movie wasn't found {"Response": "False","Error": "Movie not found!"}

    params = {
        "apikey": API_KEY,
        "s": movie_name  # s is the parameter for searching a movie by title
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        # this shall ensure a more stable request
        response.raise_for_status()
        movie_data = response.json()
        if movie_data.get("Response") == "True":
            return movie_data
        else:
            return {}
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return {}