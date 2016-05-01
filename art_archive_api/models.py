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

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'death_year': self.death_year,
            'country': self.country,
            'genre': self.genre,
        }

    def serialize_with_images(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'death_year': self.death_year,
            'country': self.country,
            'genre': self.genre,
            "images" : [image.serialize() for image in self.images]
        }


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

    def serialize(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'title': self.title,
            'year': self.year,
            'description': self.description,
        }

    def serialize_with_artist(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'title': self.title,
            'year': self.year,
            'artist': self.artist.serialize(),
            'description': self.description,
        }