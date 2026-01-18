import random
from difflib import SequenceMatcher as SM
# der style test gibt mir diesen hinweis   ka warum aber das diagramm wird gezeichnet
#movies.py:3:0: E0401: Unable to import 'matplotlib.pyplot' (import-error)
import matplotlib.pyplot as plt # pylint: disable = import-error
import movie_storage as M_S
import movie_storage_sql as MSS

# atm the user will have n+1 tries 
MAX_TRY = 3

#pylint: disable = too-few-public-methods
class BColors:
  """
  A class for all used colors.
  """
  TITLE = '\033[96m'
  MENU = '\033[92m'
  WARNING = '\033[91m'
  INPUT = '\033[94m'
  INFO = '\033[96m'
  RESET = '\033[0m'


def get_user_input(text):
  """
  A possible input with a given text.
  """
  return input(text)


def get_menu_option_from_user(menu_lenght):
  """
  This function will return an int value which will fit the menu options
  """
  try:
    user_input = int(get_user_input(
      f"{BColors.INPUT}Enter choice (0-{menu_lenght - 1}):"))
    if 0 <= user_input <= menu_lenght - 1:
      return user_input
    print(f"{BColors.INFO}Enter a number (0-{menu_lenght - 1}):")
    return get_menu_option_from_user(menu_lenght)
  except ValueError:
    print(f"{BColors.INFO}Enter a number (0-{menu_lenght - 1}):")
    return get_menu_option_from_user(menu_lenght)


def get_movie_name_from_user():
  """
  A simple input of a possible movie name.
  """
  user_input = get_user_input(BColors.INPUT + "Enter the name of movie: ")
  if user_input == "" or user_input.isspace():
    print(BColors.INFO + "Empty strings not allowed:")
    user_input = get_movie_name_from_user()
  return user_input


def get_movie_rating_from_user(text, allow_empty_string):
  """
  This function will return a possible rating.
  """
  start = 1
  end = 10
  if allow_empty_string:
    user_input = get_user_input(f'{BColors.INPUT}{text}: ')
  else:
    user_input = get_user_input(f'{BColors.INPUT}{text}({start}-{end}): ')
  if allow_empty_string:
    if user_input == "" or user_input.isspace():
      #the lowest rating
      return 1
  if "," in user_input:
      user_input = user_input.replace(",", ".")
  try:
    user_input = float(user_input)
    if start <= user_input <= end:
      return user_input
    print(f'{BColors.INFO}Enter a number ({start}-{end}): ')
    return get_movie_rating_from_user(text, allow_empty_string)
  except ValueError:
    print(f'{BColors.INFO}Enter a number ({start}-{end}): ')
    return get_movie_rating_from_user(text, allow_empty_string)


def get_movie_year_from_user(text, allow_empty_string):
  """
  A simple input of a possible year even negative ones.
  """
  user_input = get_user_input(f'{BColors.INPUT}{text}')
  if allow_empty_string:
    if user_input == "" or user_input.isspace():
      return user_input
  try:
    # im fine with all int values
    user_input = int(user_input)
    return user_input
  except ValueError:
    print(BColors.INFO + "Enter a number:")
    return get_movie_year_from_user(text,allow_empty_string)


def get_file_name_from_user():
  """
  This function will return file name.
  """
  user_input = get_user_input(BColors.INPUT + "Enter file name:")
  if user_input == "" or user_input.isspace():
    print(BColors.INFO + "Empty strings not allowed:")
    user_input = get_file_name_from_user()
  return user_input


def get_to_main_menu():
  """
  This function shall ensure the user to get back to main menu.
  """
  print()
  get_user_input(BColors.MENU + "Press enter to get to main menu.")
  print()


def print_title(title):
  """
  This function print the title.
  """
  print(f"{BColors.TITLE}********** {title} **********\n")


def print_movie_exist(movie_name, this_movie_exist):
  """
  This function prints a warning if a movie exist or not.
  """
  if this_movie_exist:
    print(f'{BColors.WARNING}The movie: "{movie_name}" allready exists')
  else:
    print(f'{BColors.WARNING}The movie: "{movie_name}" does not exist')


def show_main_menu(menu_list):
  """
  This function prints the main menu
  """
  print(BColors.MENU + "Menu:")
  for i, menu in enumerate(menu_list):
    print(f"{BColors.MENU}{i}. {menu}")


def does_this_movie_exist(movies, movie_name):
  """
  This function does a simple check if a movie exist.
  """
  return MSS.does_this_movie_exist(movie_name)

def print_movies(movies):
  """
  This function will list all movies.
  """
  print(f"{BColors.INFO}{len(movies)} movies in total.")
  for key, value in movies.items():
    print(f"{BColors.INFO}{key} ({value['year']}): {value['rating']:.1f}")


def add_movie(movies):
  """
  This function will add a new movie.
  """
  movie_name = get_movie_name_from_user()
  if not does_this_movie_exist(movies, movie_name):
    movie_rating = get_movie_rating_from_user("Enter movie rating", False)
    movie_year = get_movie_year_from_user("Enter new movie year: ", False)
    MSS.add_movie(movie_name, movie_year, movie_rating)
    print(f'{BColors.INFO}Added "{movie_name}" to database.')
    return
  print_movie_exist(movie_name,True)
  #hopefully he will get a name
  add_movie(movies)


def update_movie(movies):
  """
  This function will update a movie. ATM just the rating
  """
  count = 0
  while count <= MAX_TRY:
    count += 1
    movie_name = get_movie_name_from_user()
    if does_this_movie_exist(movies, movie_name):
      movie_rating = get_movie_rating_from_user("Enter movie rating: ", False)
      MSS.update_movie(movie_name,movie_rating)
      print(f'{BColors.INFO}Changed movie rating from "{movie_name}" to: {movie_rating}')
      return
    if count == MAX_TRY:
      print(f'{BColors.WARNING}You tried to often!')
      return
    search_movie(movies, movie_name, False)


def delete_movie(movies):
  """
  This function will delete a movie.
  """
  count = 0
  while count <= MAX_TRY:
    movie_name = get_movie_name_from_user()
    if does_this_movie_exist(movies, movie_name):
      MSS.delete_movie(movie_name)
      print(f'{BColors.INFO}Removed the movie: "{movie_name}" from database.')
      return
    if count == MAX_TRY:
      print(f'{BColors.WARNING}You tried to often!')
      return
    search_movie(movies, movie_name, False)
    count +=1


def print_show_stats(movies):
  """
  This function will show some stats of the movies.
  """
  print_average(movies)
  print_median(movies)
  print_best_movie(movies, True)
  print_best_movie(movies, False)


def print_random_movie(movies):
  """
  This function will suggest a random movie
  """
  list_of_movies_keys = movies.keys()
  movie_name = random.choice(list(list_of_movies_keys))
  movie = movies[movie_name]
  movie_rating = movie["rating"]
  print(f'{BColors.INFO}This will be your movie: '
    f'"{movie_name}" with a rating of: {movie_rating:.1f}')


def search_movie(movies, movie_name, is_searched_by_user):
  """
  This function search for a movie name.
  """
  if is_searched_by_user:
    perfect_match = does_this_movie_exist(movies, movie_name)
    if perfect_match:
      print(f'{BColors.INFO}You got the movie '
          f'"{movie_name}" with a rating of: {movies[movie_name]["rating"]:.1f}')
      print()
      return
  movie_list = get_suggested_movie_list(movies, movie_name)
  length = len(movie_list)
  if length == 0:
    print(f'{BColors.INFO}Nothing found:')
    if is_searched_by_user:
      #user has to search till he finds something
      search_movie_by_user(movies)
  if length > 0:
    print(f'{BColors.INFO}The movie {movie_name} does not exist. Did you mean:')
    if is_searched_by_user:
      for movie in movie_list:
        print(f'{BColors.INFO}{movie}, {movies[movie]["rating"]:.1f}')
    else:
      for movie in movie_list:
        print(f'{BColors.INFO}{movie}')


def get_suggested_movie_list(movies, movie_name):
  """
  This function will return a list of possible movie names
  """
  key_lower = ""
  movie_list = []
  for key in movies.keys():
    if movie_name == key:
      continue
    key_lower = key.lower()
    # im not so happy with this compare_value but it helps
    compare_value = SM(None,movie_name,key_lower).ratio()
    if movie_name in key_lower:
      movie_list.append(key)
    elif compare_value > 0.3:
      movie_list.append(key)
  return movie_list


def search_movie_by_user(movies):
  """
  This function search for a movie name by a given user input.
  """
  movie_name = get_user_input(BColors.INPUT + "Enter part of movie name: ").lower()
  search_movie(movies, movie_name, True)


def print_top_n_movies(movies):
  """
  This function prints all movies ranked by rating.
  """
  sort_by = lambda movie_name: movies[movie_name]["rating"]
  best_movies = sorted(movies, key = sort_by, reverse = True)
  print(BColors.INFO + "The top movies are:")
  for movie in best_movies:
    print(f'{BColors.INFO}{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]:.1f}')


def print_movies_sorted_by_release(movies):
  """
  This function will print all movies sorted by year
  """
  sort_by_release = True
  count = 0
  while count <= MAX_TRY:
    user_input = get_user_input(f'{BColors.INPUT}Get by latest release(Y/N)').lower()
    if user_input in ("n", "y"):
      if user_input == "n":
        sort_by_release = False
      break
    else:
      if count == MAX_TRY:
        print(f'{BColors.WARNING}You tried to often!')
        return
      print(f'{BColors.INFO}Enter (Y/N)')
    count += 1
  sort_by = lambda movie_name: movies[movie_name]["year"]
  sorted_by_year = sorted(movies, key = sort_by, reverse = sort_by_release)
  for movie in sorted_by_year:
    print(f'{BColors.INFO}{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]:.1f}')


def filter_movies(movies):
  """
  This function shall allow the user to filter movies by rating and year.
  """
  rating_text = "Enter minimum rating (leave blank for no minimum rating)"
  start_year_text = "Enter start year (leave blank for no start year)"
  end_year_text = "Enter end year (leave blank for no end year)"
  has_start_year = True
  has_end_year = True

  user_input_rating = get_movie_rating_from_user(rating_text, True)
  filter_by = lambda movie_name : movies[movie_name]["rating"] >= user_input_rating
  #all movie names with the needed rating
  new_movies = list(filter(filter_by, movies))

  user_input_start_year = get_movie_year_from_user(start_year_text, True)
  if isinstance(user_input_start_year, str):
    has_start_year = False
  user_input_end_year = get_movie_year_from_user(end_year_text, True)
  if isinstance(user_input_end_year, str):
    has_end_year = False
  for movie in new_movies:
    movie_year = movies[movie]["year"]
    if has_start_year and has_end_year:
      if user_input_start_year <= movie_year <= user_input_end_year:
        print(f'{BColors.INFO}{movie} ({movie_year}): {movies[movie]["rating"]:.1f}')
    elif has_start_year and not has_end_year:
      if user_input_start_year <= movie_year:
        print(f'{BColors.INFO}{movie} ({movie_year}): {movies[movie]["rating"]:.1f}')
    elif not has_start_year and has_end_year:
      if movie_year <= user_input_end_year:
        print(f'{BColors.INFO}{movie} ({movie_year}): {movies[movie]["rating"]:.1f}')
    else:
      print(f'{BColors.INFO}{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]:.1f}')


def create_valuation_histogram(movies):
  """
  This function creates a valuation histogram file.
  """
  list_of_ratings = [movies[movie_name]["rating"] for movie_name in movies]
  plt.hist(list_of_ratings, bins = "auto")
  plt.title("Movie")
  plt.xlabel("Movie Rating")
  plt.ylabel("Frequency")
  plt.savefig(get_file_name_from_user())
  plt.close()


def print_average(movies):
  """
  This function determines the average rating of all movies.
  """
  average = 0.0
  for movie in movies:
    average += movies[movie]["rating"]
  average = average/len(movies)
  print(f"{BColors.INFO}The average rating of all movies is: {average:.1f}")


def print_median(movies):
  """
  This function prints the median.
  """
  median = get_median(movies)
  print(f"{BColors.INFO}The median is: {median:.1f}")


def get_median(movies):
  """
  This function determines the median about all given movies
  """
  list_of_ratings = [movies[movie_name]["rating"] for movie_name in movies]
  list_of_ratings = sorted(list_of_ratings)
  median = 0
  list_length = len(movies)
  if list_length % 2 == 0:
    med1 = list_of_ratings[list_length // 2 - 1]
    med2 = list_of_ratings[list_length // 2]
    median = (med1 + med2) / 2
  else:
    median = list_of_ratings[list_length // 2]
  return median


def print_best_movie(movies, print_the_best):
  """
  This function prints the best or worst movies.
  """
  best_movies = get_best_movie(movies,print_the_best)
  best_rating = movies[best_movies[0]]["rating"]
  some_string = ""
  if print_the_best:
    some_string = "best"
  else:
    some_string = "worst"
  for i, movie in enumerate(best_movies):
    if len(best_movies) == 1:
      print(f'{BColors.INFO}The {some_string} movie by rating is: '
            f'"{movie}" with a rating of: {best_rating:.1f}')
    else:
      if i == 0:
        print(f"{BColors.INFO}The {some_string} {len(best_movies)} "
              f"movies with a rating of: {best_rating:.1f}")
      print(f"{BColors.INFO}{movie}")
  print()


def get_best_movie(movies, return_best):
  """
  This function returns all movies with the highest or lowest rating
  """
  best_movies = []
  best_rating = 0.0
  if return_best:
    for movie in movies:
      value = movies[movie]["rating"]
      if best_rating < value:
        best_movies = []
        best_rating = value
        best_movies.append(movie)
      elif best_rating == value:
        best_movies.append(movie)
  else:
    best_rating = 11
    for movie in movies:
      value = movies[movie]["rating"]
      if best_rating > value:
        best_movies = []
        best_rating = value
        best_movies.append(movie)
      elif best_rating == value:
        best_movies.append(movie)
  return best_movies


def get_main_menu_options():
  """
  The main menu options.
  """
  main_menu_options = ["Exit", "List movie", "Add movie", "Delete movie",
  "Update movie", "Stats", "Random movie", "Search movie",
  "Movies sorted by rating", "Movies sorted by release",
  "Filter movies", "Create valuation histogram", "Generate website"
  ]
  return main_menu_options


def generate_website(movies):
  """
  This function will generate a website.
  """
  #TODO just implement it
  print("Successfully generated the website.")


def handle_input(movies, user_input):
  """
  This function handles most of the main menu option.
  no dispatch pattern atm
  """
  if user_input == 1:
    print_movies(movies)
  elif user_input == 3:
    delete_movie(movies)
  elif user_input == 4:
    update_movie(movies)
  elif user_input == 5:
    print_show_stats(movies)
  elif user_input == 6:
    print_random_movie(movies)
  elif user_input == 7:
    search_movie_by_user(movies)
  elif user_input == 8:
    print_top_n_movies(movies)
  elif user_input == 9:
    print_movies_sorted_by_release(movies)
  elif user_input == 10:
    filter_movies(movies)
  elif user_input == 11:
    create_valuation_histogram(movies)
  elif user_input == 12:
    generate_website(movies)
  else:
    print(BColors.WARNING + "This should not happen!")


def main():
  """
  The main function of this py.
  """
  movies = MSS.get_list_of_movies()
  main_menu_options = get_main_menu_options()
  print_title("My movie database")
  while True:
    there_is_a_movie = len(movies) > 0
    show_main_menu(main_menu_options)
    user_input = get_menu_option_from_user(len(main_menu_options))
    print()
    if user_input == 0:
      print(f"{BColors.INFO}Bye!{BColors.RESET}")
      break
    if user_input == 2:
      add_movie(movies)
      get_to_main_menu()
      continue
    if there_is_a_movie:
      handle_input(movies, user_input)
    else:
      print(BColors.INFO + "There is no movie at database you can just add a new one.")
    get_to_main_menu()


if __name__ == "__main__":
  main()
