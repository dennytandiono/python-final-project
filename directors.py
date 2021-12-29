from config import db
from flask import make_response, abort
from models import Directors, DirectorSchema,Movies

def read_all():
    """
    This function responds to a request for /api/director
    with the complete lists of director
    :return:        json string of list of director
    """
    # Create the list of director from our data
    director = Directors.query.order_by(Directors.name).limit(10)

    # Serialize the data for the response
    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(director)
    return data

def read_one(director_id):
    """
    This function responds to a request for /api/director/{director_id}
    with one matching director from director
    :param director_id:   Id of director to find
    :return:            director matching id
    """
    # Build the initial query
    director = (Directors.query.filter(
        Directors.id== director_id).outerjoin(Movies).one_or_none())

    # Did we find a director?
    if director is not None:

        # Serialize the data for the response
        director_schema = DirectorSchema()
        data = director_schema.dump(director)
        return data

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {director_id}")

def read_director_by_name(director_name):
    """
    This function responds to a request for /api/directors/director_name
    with a record of director filtered by their name
    :param director_name:  Director name to be filtered
    :return: json of a director record
    """

    search = "%{}%".format(director_name)

    director = (
        Directors.query.filter(Directors.name.like(search)).all()
    )

    if director is not None:
        director_schema = DirectorSchema(many=True)
        data = director_schema.dump(director)
        return data
    
    else:
        abort(404, f"Director not found for name: {director_name}")

def create(director):
    """
    This function creates a new director in the director structure
    based on the passed in director data
    :param director:  director to create in director structure
    :return:        201 on success, 406 on director exists
    """
    uid = director.get("uid")

    existing_uid = (Directors.query.filter(Directors.uid == uid).one_or_none())

    if existing_uid is None:

        # Create a director instance using the schema and the passed in director
        schema = DirectorSchema()
        new_uid = schema.load(director, session=db.session)

        # Add the director to the database
        db.session.add(new_uid)
        db.session.commit()

        # Serialize and return the newly created director in the response
        data = schema.dump(new_uid)

        return data, 201

    # Otherwise, nope, director exists already
    else:
        abort(409, f"Director {uid} exists already")

def update(director_id, director):
    """
    This function updates an existing director in the director structure
    :param director_id:   Id of the director to update in the director structure
    :param director:      director to update
    :return:            updated director structure
    """
    # Get the director requested from the db into session
    update_director = Directors.query.filter(
        Directors.id == director_id).one_or_none()

    # Did we find an existing director?
    if update_director is not None:

        # turn the passed in director into a db object
        schema = DirectorSchema()
        update = schema.load(director, session=db.session)

        # Set the id to the director we want to update
        update.director_id = update_director.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated director in the response
        data = schema.dump(update_director)

        return data, 200

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {director_id}")



def delete(director_id):
    """
    This function deletes a director from the director structure
    :param director_id:   Id of the director to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the director requested
    director = Directors.query.filter(Directors.id == director_id).one_or_none()

    # Did we find a director?
    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(f"Director {director_id} deleted", 200)

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {director_id}")

