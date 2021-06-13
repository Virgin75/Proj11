import json


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


competitions = load_competitions()
clubs = load_clubs()


def update_club_points(club_index_in_json, new_points_tally):
    clubs[club_index_in_json]['points'] = new_points_tally
    new_json = {}
    new_json['clubs'] = clubs
    with open("clubs.json", "w") as jsonFile:
        json.dump(new_json, jsonFile)


def update_competition_places(competition_index_in_json, new_places_tally):
    competitions[competition_index_in_json]['numberOfPlaces'] = new_places_tally
    new_json = {}
    new_json['competitions'] = competitions
    with open("competitions.json", "w") as jsonFile:
        json.dump(new_json, jsonFile)
