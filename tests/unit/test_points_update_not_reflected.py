from ...server import app
from ...db import competitions, clubs
from datetime import datetime

from ...db import update_club_points, update_competition_places


def test_points_update_not_reflected():
    """
    WHEN the '/purchasePlaces' page is requested (POST) with valid data
    THEN the amount of points used should be deducted from the club's balance.
    """
    CLUB_TO_TEST = 'She Lifts'
    COMPETITION_TO_TEST = 'Spring Festival'
    PLACES_TO_BUY = 4

    update_club_points(next(i for i, club in enumerate(clubs)
                            if club["name"] == CLUB_TO_TEST), 15)
    update_competition_places(next(i for i, comp in enumerate(competitions)
                                   if comp["name"] == COMPETITION_TO_TEST), 14)

    club_points_before_request = 15

    with app.test_client() as test_client:
        response = test_client.post('/purchasePlaces', data=dict(
            club=CLUB_TO_TEST,
            competition=COMPETITION_TO_TEST,
            places=PLACES_TO_BUY
        ))

    current_club_points = next(club for club in clubs if club['name'] == CLUB_TO_TEST)['points']

    assert response.status_code == 200
    assert club_points_before_request - (3*PLACES_TO_BUY) == current_club_points
