

def get_template_as_string(path):
    """
    This function returns the given template as string.
    """
    with open(path, "r") as a:
        data = a.read()
    return data

def serialize_movie(movie_name, movie_data):
    """
    This function serialize a movie.
    """
    #havnt found/seen a rating at website so just 3 values are needed
    year = movie_data.get("year")
    url = movie_data.get("image_url")
    return f"""
    <li>
    <div class="movie">
        <img class="movie-poster" src="{url}" alt="No image available">
        <div class="movie-title">{movie_name}</div>
        <div class="movie-year">{year}</div>
    </div>
    </li>
    """


def get_movies_as_string(movies):
    """
    This function creates a string of all movies.
    """
    movie_list = []
    for movie_name, movie_data in movies.items():
        movie_list.append(serialize_movie(movie_name, movie_data))
    return "".join(movie_list)


def create_html_page(path,data):
    """
    This function creates a new "html" file.
    """
    with open(path,"w")as a:
        a.write(data)


def generate_web_page(movies, title):
    template_string = get_template_as_string("index_template.html")
    movie_string = get_movies_as_string(movies)
    new_template_string = template_string.replace("__TEMPLATE_TITLE__", title)
    new_template_string = new_template_string.replace("__TEMPLATE_MOVIE_GRID__", movie_string)
    create_html_page("index.html", new_template_string)