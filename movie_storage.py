import json


def get_movies():
  """
  Returns a dictionary of dictionaries that
  contains the movies information in the database.

  The function loads the information from the JSON
  file and returns the data.

  For example, the function may return:
  {
    "Titanic": {
       "rating": 9,
      "year": 1999
     },
     "..." {
       ...
    },
  }
  """
  try:
    with open("data.json", "r") as file_obj:
      data = json.loads(file_obj.read())
    return data
  except FileNotFoundError:
    print()
    print("Given file name not found. Starting with empty database.")
    print()
    return {}


def save_movies(movies):
  """
  Gets all your movies as an argument and saves them to the JSON file.
  """
  with open("data.json", "w") as file_obj:
    json.dump(movies, file_obj, indent=2)


def add_movie(title, rating, year):
  """
  Adds a movie to the movies database.
  Loads the information from the JSON file, add the movie,
  and saves it. The function doesn't need to validate the input.
  """
  movies = get_movies()
  movies[title] = {"rating": rating, "year": year}
  save_movies(movies)


def delete_movie(title):
  """
  Deletes a movie from the movies database.
  Loads the information from the JSON file, deletes the movie,
  and saves it. The function doesn't need to validate the input.
  """
  movies = get_movies()
  movies.pop(title)
  save_movies(movies)


def update_movie(title, rating):
  """
  Updates a movie from the movies database.
  Loads the information from the JSON file, updates the movie,
  and saves it. The function doesn't need to validate the input.
  """
  movies = get_movies()
  movies[title]["rating"] = rating
  save_movies(movies)
