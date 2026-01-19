from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=False)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER,
            rating REAL,
            image_url TEXT
        )
    """))
    connection.commit()


def get_list_of_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, image_url FROM movies"))
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "image_url": row[3]} for row in movies}


def add_movie(title, year, rating, image_url=None):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO movies (title, year, rating, image_url) VALUES (:title, :year, :rating, :image_url)"),
                {"title": title, "year": year, "rating": rating, "image_url": image_url})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title =:title"),
                               {"title": title})
            connection.commit()
            print(f"Movie '{title}' was successfully deleted.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating =:rating WHERE title =:title"),
                               {"title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully to a new rating of {rating}.")
        except Exception as e:
            print(f"Error: {e}")


def check_for_movies():
    """"
    A simple check if there is anything at database
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id FROM movies LIMIT 1"))
        result = result.first()
    return result


def does_this_movie_exist(movie_name):
    """"
    A simple check if this movie exists at database
    """
    with engine.connect() as connection:
        query = text("SELECT EXISTS(SELECT id FROM movies WHERE LOWER(title) = LOWER(:title))")
        result = connection.execute(query, {'title': movie_name}).scalar()
        return result


def get_movie_rating(movie_name):
    """
    This function will return the rating of a movie
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT rating FROM movies WHERE title =:title LIMIT 1"),
                                    {'title': movie_name})
        result = result.first()
    return result


def get_possible_movie_names(movie_name):
    """
    This function will return a list of possible movie names
    """
    max_number_of_movie_names = 10
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title FROM movies WHERE title LIKE :title LIMIT :max"),
                                    {'title': f'%{movie_name}%', 'max': max_number_of_movie_names})
        result = result.fetchall()
        list_of_movie_names = []
        for row in result:
            list_of_movie_names.append(row)
    return list_of_movie_names
