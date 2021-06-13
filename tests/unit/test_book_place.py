from pythontesting import server
from pythontesting.db import clubs, competitions


def test_book_place():
    """
    GIVEN a Flask application.
    WHEN the '/purchasePlaces' page is requested (POST) with valid data
    THEN check that the response points are substracted
    """

    CLUB_TO_TEST = 'She Lifts'
    COMPETITION_TO_TEST = 'Spring Festival'
    PLACES_TO_BUY = 1

    club = [c for c in clubs if c['name'] == CLUB_TO_TEST][0]
    competition = [comp for comp in competitions if comp['name'] == COMPETITION_TO_TEST][0]

    club_points_before = club['points']
    competition_places_before = competition['numberOfPlaces']

    response = server.app.test_client().post(
        '/purchasePlaces', data=dict(
            club=CLUB_TO_TEST,
            competition=COMPETITION_TO_TEST,
            places=PLACES_TO_BUY
        ), follow_redirects=True)

    assert response.status_code == 200
    assert club['points'] == club_points_before - PLACES_TO_BUY
    assert competition['numberOfPlaces'] == competition_places_before - PLACES_TO_BUY
