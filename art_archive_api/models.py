from application import db


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    birth_year = db.Column(db.Integer)
    death_year = db.Column(db.Integer)
    country = db.Column(db.String(45))
    genre = db.Column(db.String(45))
    images = db.relationship(
        'Image',
        backref='artist',
    )


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255))
    title = db.Column(db.String(255))
    year = db.Column(db.Integer)
    artist_id = db.Column(
        db.Integer,
        db.ForeignKey('artists.id')
    )
    description = db.Column(db.String(255))