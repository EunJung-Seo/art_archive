from flask import jsonify, request

from application import app
from models import Artist


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

    # from IPython import embed;embed()

    # name parameter가 존재하는 경우
    if name:
        artists = Artist.query.filter_by(name=name)
        artists_count = artists.count()
    else: 
        artists = Artist.query.all()
        artists_count = Artist.query.count()


    # offset parameter가 유효한 경우 
    if offset >= 0 and artists_count > offset:
        if count:
            count += offset
        else:
            count = artists_count
        artists = artists[offset:count]

    # images_detail이 1인 경우
    if images_detail:
        json_list = [artist.serialize_with_images() for artist in artists]
    else:
        json_list = [artist.serialize() for artist in artists]


    return jsonify({
            "images_detail": images_detail,
            "list": json_list,
        }
    )

@app.route('/artist/<int:id>')
def get_artist(id):
    images_detail = request.args.get('images_detail', 0, type=int)

    artist = Artist.query.get_or_404(id)

    # images_detail이 1인 경우
    if images_detail:
        json_data = artist.serialize_with_images()
    else:
        json_data = artist.serialize()

    return jsonify({
            "images_detail": images_detail,
            "artist": json_data,
        }
    )
