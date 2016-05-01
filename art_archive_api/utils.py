from flask import abort


def get_artist_by_name(model, name):
    objects = []

    if name:
        objects = model.query.filter_by(name=name)
    else:
        objects = model.query
    objects_count = objects.count()
    return objects, objects_count

def slice_query_set(offset, count, objects_count, objects):
    if offset >= 0 and objects_count > offset:
        if count:
            count += offset
        else:
            count = objects_count
        objects = objects[offset:count]
    return objects

def serialize_artist(artist, images_detail):
    json_data = {}
    if images_detail:
        json_data = artist.serialize_with_images()
    else:
        json_data = artist.serialize()
    return json_data

def get_or_abort(model, object_id, code=422):
    """
    get an object with his given id or an abort error (422 is the default)
    """
    result = model.query.get(object_id)
    return result or abort(code)

def get_images_by_title(model, title):
    objects = []

    if title:
        objects = model.query.filter_by(title=title)
    else:
        objects = model.query
    return objects, objects.count()

def get_images_by_artist(model_image, model_artist, images, name):
    if name:
        images = images.join(
            model_artist,
            model_image.artist_id == model_artist.id
        ).filter(
            model_artist.name == name
        )
    return images, images.count()