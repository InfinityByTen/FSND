from app import *
'''
This file is to setup the db defined in the app a starting set of entries.
Instead of creating the db with data again and again on errors, this script,
will populate a fresh db with the same data as what came in the starter_code.
This will enable me to have a setup where I can refresh the entire local project/db
state to mint easily and start over if I mess up.
'''
guns_n_petals = Artist(
	name="Guns N Petals",
	genres="Rock n Roll",
	city="San Francisco",
	state="CA",
    phone="326-123-5000",
    website_link="https://www.gunsnpetalsband.com",
    facebook_link="https://www.facebook.com/GunsNPetals",
    seeking_venue=True,
    seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
    image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80")

matt_quevedo = Artist(
	name="Matt Quevedo",
	genres="Jazz",
    city="New York",
    state="NY",
    phone="300-400-5000",
    facebook_link="https://www.facebook.com/mattquevedo923251523",
    seeking_venue=False,
    image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80")

wild_sax = Artist(
	name="The Wild Sax Band",
    genres="Jazz,Classical",
    city="San Francisco",
    state="CA",
    phone="432-325-5432",
    seeking_venue=False,
    image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80")

db.session.add_all([guns_n_petals, matt_quevedo, wild_sax])
db.session.commit()

musical_hop=Venue(
	name="The Musical Hop",
    genres="Jazz,Reggae,Swing,Classical,Folk",
    address="1015 Folsom Street",
    city="San Francisco",
    state="CA",
    phone="123-123-1234",
    website_link="https://www.themusicalhop.com",
    facebook_link="https://www.facebook.com/TheMusicalHop",
    seeking_talent=True,
    seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
    image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60")

dueling_pianos=Venue(
	name="The Dueling Pianos Bar",
    genres="Classical,R&B,Hip-Hop",
    address="335 Delancey Street",
    city="New York",
    state="NY",
    phone="914-003-1132",
    website_link="https://www.theduelingpianos.com",
    facebook_link="https://www.facebook.com/theduelingpianos",
    seeking_talent=False,
    image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80")

park_square=Venue(
	name="Park Square Live Music & Coffee",
    genres="Rock n Roll,Jazz,Classical,Folk",
    address="34 Whiskey Moore Ave",
    city="San Francisco",
    state="CA",
    phone="415-000-1234",
    website_link="https://www.parksquarelivemusicandcoffee.com",
    facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    seeking_talent=False,
    image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80")

db.session.add_all([musical_hop, dueling_pianos, park_square])
db.session.commit()

show1 = Show( musical_hop, guns_n_petals, "2019-05-21T21:30:00.000Z")
show2 = Show( matt_quevedo, park_square, "2019-06-15T23:00:00.000Z")
show3 = Show( wild_sax, park_square, "2035-04-01T20:00:00.000Z")
show4 = Show( wild_sax, park_square, "2035-04-08T20:00:00.000Z")
show5 = Show( wild_sax, park_square, "2035-04-15T20:00:00.000Z")
db.session.add_all([show1, show2, show3, show4, show5])
db.session.commit()