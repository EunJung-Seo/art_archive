from flask import abort


def get_by_name_or_all(model, name):
    objects = []
    objects_count = 0

    if name:
        objects = model.query.filter_by(name=name)
        objects_count = objects.count()
    else:
        objects = model.query.all()
        objects_count = model.query.count()
    return objects, objects_count

def slice_query_set(offset, count, objects_count, objects):
    if offset >= 0 and objects_count > offset:
        if count:
            count += offset
        else:
            count = objects_count
        objects = objects[offset:count]

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