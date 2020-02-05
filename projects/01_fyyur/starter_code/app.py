#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from config import *
from flask_migrate import Migrate
from copy import copy
from sqlalchemy import func, distinct
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    # Self TODO: see if description state should be dependent on the bool value
    seeking_description = db.Column(db.String(240))
    show_ref = db.relationship('Show', backref='venue',
                               lazy=True)

    def __repr__(self):
        return f'<Venue {self.id}: "{self.name}", in ({self.city}, {self.state})>'

    def __str__(self):
        return f"""<Venue
      id: {self.id},
      name: {self.name},
      city: {self.city},
      state: {self.state}
      address: {self.address if self.address is not None else "No address available"}
      genres: {self.genres}
      phone: {self.phone if self.phone is not None else "No Phone Available"}
      seeking_talent: {self.seeking_talent}
      seeking_description: {self.seeking_description if self.seeking_description is not None else "None"}
      image_link:{"Available" if self.image_link is not None else "Not Available"}
      facebook_link: {"Available" if self.facebook_link is not None else "Not Available"}
      website_link: {"Available" if self.website_link is not None else "Not Available"}
      >"""


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(240))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    show_ref = db.relationship('Show', backref='artist',
                               lazy=True)

    def __repr__(self):
        return f'<Artist {self.id}: "{self.name}", from ({self.city}, {self.state})>'

    def __str__(self):
        return f"""<Artist
      id: {self.id},
      name: {self.name},
      city: {self.city},
      state: {self.state}
      genres: {self.genres}
      phone: {self.phone if self.phone is not None else "No Phone Available"}
      seeking_venue: {self.seeking_venue}
      seeking_description: {self.seeking_description if self.seeking_description is not None else "None"}
      image_link:{"Available" if self.image_link is not None else "Not Available"}
      facebook_link: {"Available" if self.facebook_link is not None else "Not Available"}
      website_link: {"Available" if self.website_link is not None else "Not Available"}
      >"""


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'),
                         nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'),
                          nullable=False)

    def __init__(self, artist, venue, time=None):
        self.venue_id = venue.id
        self.artist_id = artist.id
        self.start_time = time or datetime.now()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

    # num_shows should be aggregated based on number of upcoming shows per
    # venue
    venue_data = db.session.query(Venue.city,
                                  Venue.state,
                                  Venue.id,
                                  Venue.name,
                                  func.count(Show.id).filter(
                                      Show.start_time >= datetime.utcnow())
                                  .label("num_upcoming_shows"))\
        .outerjoin(Show).group_by(Venue)

    def get_venues_for_location(city, state):
        venues_list = []
        aggregated_shows = 0
        for venue in venue_data.filter(Venue.city == city, Venue.state == state).all():
            venues_list.append(venue)
            # To order the location in the main view
            aggregated_shows += venue.num_upcoming_shows
        return venues_list, aggregated_shows

    data = []
    unique_locations = db.session.query(
        Venue.city, Venue.state).distinct(Venue.city, Venue.state)
    for entry in unique_locations.all():
        location = entry._asdict()
        data.append(location)
        data[-1]['venues'], data[-1]['aggregated_shows'] = get_venues_for_location(
            location["city"], location["state"])

    data.sort(key=lambda x: x['aggregated_shows'], reverse=True)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live
    # Music & Coffee"
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


def get_show_info_for_artist(shows):
    show_info = []
    for show in shows:
        show_info.append(show[1].__dict__.copy())
        show_info[-1]['artist_id'] = show[2].id
        show_info[-1]['artist_name'] = show[2].name
        show_info[-1]['artist_image_link'] = show[2].image_link
        show_info[-1]['start_time'] = babel.dates.format_datetime(
            show_info[-1]['start_time'], "yyyy-MM-dd HH:mm:ss")
    return show_info


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id

    venue_data = Venue.query.get(venue_id).__dict__
    # self TODO: more elegant way?
    venue_data['genres'] = venue_data['genres'].split(',')
    # self TODO: see if renaming the column is a better idea
    venue_data['website'] = venue_data.pop('website_link')

    shows = db.session.query(Venue, Show, Artist).join(
        Venue).join(Artist).filter(Show.venue_id == venue_id)

    upcoming = shows.filter(Show.start_time >= datetime.utcnow())
    venue_data['upcoming_shows_count'] = upcoming.count()
    venue_data['upcoming_shows'] = get_show_info_for_artist(upcoming)

    past = shows.filter(Show.start_time < datetime.utcnow())
    venue_data['past_shows_count'] = past.count()
    venue_data['past_shows'] = get_show_info_for_artist(past)

    return render_template('pages/show_venue.html', venue=venue_data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit
    # could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the
    # homepage
    return None

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    return render_template('pages/artists.html', artists=Artist.query.all())


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


def get_show_info_for_venue(shows):
    show_info = []
    for show in shows:
        show_info.append(show[1].__dict__.copy())
        show_info[-1]['venue_id'] = show[2].id
        show_info[-1]['venue_name'] = show[2].name
        show_info[-1]['venue_image_link'] = show[2].image_link
        show_info[-1]['start_time'] = babel.dates.format_datetime(
            show_info[-1]['start_time'], "yyyy-MM-dd HH:mm:ss")
    return show_info


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
        # shows the venue page with the given venue_id
    artist_data = Artist.query.get(artist_id).__dict__
    artist_data['genres'] = artist_data['genres'].split(',')
    artist_data['website'] = artist_data.pop('website_link')

    shows = db.session.query(
        Artist, Show, Venue).join(Artist).join(Venue).filter(Show.artist_id == artist_id)
    upcoming = shows.filter(Show.start_time >= datetime.utcnow())
    artist_data['upcoming_shows_count'] = upcoming.count()
    artist_data['upcoming_shows'] = get_show_info_for_venue(upcoming)

    past = shows.filter(Show.start_time < datetime.utcnow())
    artist_data['past_shows_count'] = past.count()
    artist_data['past_shows'] = get_show_info_for_venue(past)

    return render_template('pages/show_artist.html', artist=artist_data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be
    # listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    query = db.session.query(Venue.id.label("venue_id"),
                             Venue.name.label("venue_name"),
                             Artist.id.label("artist_id"),
                             Artist.name.label("artist_name"),
                             Artist.image_link.label("artist_image_link"),
                             Show.start_time).join(Venue).join(Artist).all()

    def transform_info(result):
        result = result._asdict()
        result['start_time'] = babel.dates.format_datetime(
            result['start_time'], "yyyy-MM-dd HH:mm:ss")
        return result

    data = list(map(lambda x: transform_info(x), query))
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
