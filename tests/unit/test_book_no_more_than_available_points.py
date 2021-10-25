import random

from ...server import app
from ...db import clubs, competitions
from ...db import update_club_points, update_competition_places


def test_book_no_more_than_available_points():
    """
    WHEN the '/purchasePlaces' page is requested (POST) with valid data
    THEN check that the club have enough points
    """

    CLUB_TO_TEST = 'Iron Temple'
    COMPETITION_TO_TEST = 'Spring Festival'
    PLACES_TO_BUY = random.randint(1, 2)

    update_club_points(next(i for i, club in enumerate(clubs)
                            if club["name"] == CLUB_TO_TEST), 15)
    update_competition_places(next(i for i, comp in enumerate(competitions)
                                   if comp["name"] == COMPETITION_TO_TEST), 14)

    club = [c for c in clubs if c['name'] == CLUB_TO_TEST][0]

    club_points_before = club['points']

    with app.test_client() as test_client:
        response = test_client.post(
            '/purchasePlaces', data=dict(
                club=CLUB_TO_TEST,
                competition=COMPETITION_TO_TEST,
                places=PLACES_TO_BUY
            ), follow_redirects=True)

    assert response.status_code == 200

    if (PLACES_TO_BUY > club_points_before):
        assert b"Not enough points available in the club to book that many places" in response.data
    else:
        assert b"Great-booking complete!" in response.data
