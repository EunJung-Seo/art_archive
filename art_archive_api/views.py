from flask import jsonify, request

from application import app
from models import Artist, Image
from utils import *


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/artists/')
def get_artists():
    artists = []
    artists_count = 0

    name = request.args.get('name')
    offset = request.args.get('offset', 0, type=int)
    count = request.args.get('count', 0, type=int)
    images_detail = request.args.get('images_detail', 0, type=int)

    artists, artists_count = get_by_name_or_all(Artist, name)

    artists = slice_query_set(offset, count, artists_count, artists)

    json_list = [
        serialize_artist(artist, images_detail) 
        for artist in artists
    ]

    return jsonify({
            "images_detail": images_detail,
            "list": json_list,
        }
    )

@app.route('/artist/<int:id>')
def get_artist(id):
    images_detail = request.args.get('images_detail', 0, type=int)

    artist = get_or_abort(Artist, id)
    json_data = serialize_artist(artist, images_detail)

    return jsonify({
            "images_detail": images_detail,
            "artist": json_data,
        }
    )

@app.route('/images/')
def get_images():
    images = []
    images_count = 0

    artist_name = request.args.get('artist')
    title = request.args.get('title')
    offset = request.args.get('offset', 0, type=int)
    count = request.args.get('count', 0, type=int)

    images, images_count = get_images_by_title(Image, title)
    images, images_count = get_images_by_artist(Image, Artist, images, artist_name)
    images = slice_query_set(offset, count, images_count, images)

    json_list = [
        image.serialize_with_artist()
        for image in images
    ]

    return jsonify({"list": json_list})

# Error Response
@app.errorhandler(404)
def page_not_found(error):
    response = jsonify({'error': 'Not Found'})
    response.status_code = 404
    return response

@app.errorhandler(422)
def unprocessable_entity(error):
    response = jsonify({'error': 'Unprocessable Entity'})
    response.status_code = 422
    return response

@app.errorhandler(500)
def internal_server_error(error):
    response = jsonify({'error': 'Internal Server Error'})
    response.status_code = 500
    return response