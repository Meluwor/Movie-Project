def get_valid_movie_year(movie_year):
    """
    This function shall ensure to get a year like 2000 or 2015.
    The API somtimes provides this 'year' as string interval  like 2000-2005
    I hope this will be the only kind of interval type
    """
    try:
        year = str(movie_year).strip()[:4]
        return int(year)
    # maybe none so I need type error as well
    except (ValueError, TypeError):
        return None

def get_valid_movie_rating(rating):
    """
    This function shall ensure to get a proper rating(float) for database if possible.
    """
    try:
        return float(rating)
    #maybe none so I need type error as well
    except (ValueError, TypeError):
        return None


def get_valid_image_url(url):
    """
    This function shall ensure to get a string(URL) if possible
    """
    if isinstance(url, str):
        url = url.strip()
        if url.upper() != "N/A" and url != "":
            return url
    return None


def transform_movie_data(movie_data):
    """
    This function will transform the data from API to a proper format for the database.
    """
    if movie_data:
        #I expect a name for each movie else it should never have been found
        movie_title = movie_data.get("Title")
        movie_year = get_valid_movie_year(movie_data.get("Year"))
        movie_rating = get_valid_movie_rating(movie_data.get("imdbRating"))
        movie_img_url = get_valid_image_url(movie_data.get("Poster"))

        new_movie = {"title": movie_title, "year": movie_year, "rating": movie_rating, "image_url": movie_img_url}
        return new_movie
    return {}
