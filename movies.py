from config import db
from flask import make_response, abort
from models import Directors, MovieSchema,Movies

def read_all():
    """
    This function responds to a request for /api/movie
    with the complete lists of movie
    :return:        json string of list of movie
    """
    # Create the list of movie from our data
    movie = Movies.query.order_by(db.desc(Movies.vote_average)).limit(10)

    # Serialize the data for the response
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movie)
    return data


def read_top_popularity(limit = 5):
    """
    This function responds to a request for /api/movie
    with the complete lists of movie
    :return:        json string of list of movie
    """
    # Create the list of movie from our data
    movie = Movies.query.order_by(db.desc(Movies.popularity)).limit(limit)

    # Serialize the data for the response
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movie)
    return data


def read_highest_budget(limit = 5):
    """
    This function responds to a request for /api/movie
    with the complete lists of movie
    :return:        json string of list of movie
    """
    # Create the list of movie from our data
    movie = Movies.query.order_by(db.desc(Movies.budget)).limit(limit)

    # Serialize the data for the response
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movie)
    return data



def read_one(director_id, movie_id):
    """
    This function responds to a request for api/director/{director_id}/movies/{movie_id}
    with one matching movie from movie
    :param director_id:   Id of director to find
    :param movie_id : Id of movie to find
    :return:            movie matching id
    """
    # Build the initial query
    movie = (Movies.query.join(Directors, Directors.id == Movies.director_id).filter(
        Directors.id == director_id).filter(
        Movies.id == movie_id).one_or_none())

    # Did we find a movie?
    if movie is not None:

        # Serialize the data for the response
        movie_schema = MovieSchema()
        data = movie_schema.dump(movie)
        return data

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movie not found for Id: {movie_id}")

def create(director_id, movie):
    """
    This function creates a new movie in the movie structure
    based on the passed in movie data
    :param director_id:   Id of director to create
    :param movie:  movie to create in movie structure
    :return:        201 on success, 406 on movie exists
    """

    director = Directors.query.filter(Directors.id == director_id).one_or_none()

    if director is None:
        abort(404, f"Director not found for Id: {director_id}")

    # Create a movie instance using the schema and the passed in movie
    schema = MovieSchema()
    new_movie = schema.load(movie, session=db.session)

    # Add the movie to the database
    director.movies.append(new_movie)
    db.session.commit()

    # Serialize and return the newly created movie in the response
    data = schema.dump(new_movie)
    return data, 201



def update(director_id, movie_id, movie):
    """
    This function updates an existing movie in the movie structure
    :param director_id:   Id of the director to update in the movie structure
    :param movie_id:   Id of the movie to update in the movie structure
    :param movie:      movie to update
    :return:            updated movie structure
    """
    # Get the movie requested from the db into session
    update_movie = (Movies.query.filter(Movies.director_id == director_id).filter(
        Movies.id == movie_id).one_or_none())

    # Did we find an existing movie?
    if update_movie is not None:

        # turn the passed in movie into a db object
        schema = MovieSchema()
        update = schema.load(movie, session=db.session)

        # Set the id to the movie we want to update
        update.director_id = update_movie.director_id
        update.id = update_movie.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated movie in the response
        data = schema.dump(update_movie)

        return data, 200

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movie not found for Id: {movie_id}")



def delete(director_id, movie_id):
    """
    This function deletes a movie from the movie structure
    :param director_id:   Id of the director to delete
    :param movie_id:   Id of the movie to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the movie requested
    movie = (Movies.query.filter(Movies.director_id == director_id).filter(
        Movies.id == movie_id).one_or_none())

    # Did we find a movie?
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response("Movie {movie_id} deleted".format(movie_id=movie_id),
                             200)

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movie not found for Id: {movie_id}")

