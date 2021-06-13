from flask import Flask, render_template, request, redirect, flash, url_for
from .db import (competitions,
                 clubs,
                 update_club_points,
                 update_competition_places)


app = Flask(__name__)
app.secret_key = 'something_special'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show-summary', methods=['POST'])
def show_summary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        return "Sorry but this email does not exist :("


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html',
                               club=found_club,
                               competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [(index, c) for index, c in enumerate(competitions) if c['name'] == request.form['competition']][0]
    club = [(index, c) for index, c in enumerate(clubs) if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])

    # Update places left in competition and points left of the club
    competition[1]['numberOfPlaces'] = int(competition[1]['numberOfPlaces']) - places_required
    club[1]['points'] = int(club[1]['points']) - places_required
    update_club_points(club[0], club[1]['points'])
    update_competition_places(competition[0], competition[1]['numberOfPlaces'])
    print(competitions[1])
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club[1], competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
