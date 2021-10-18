import random
from pythontesting import server
from pythontesting.db import clubs, competitions


def test_book_no_more_than_available_points():
    """
    WHEN the '/purchasePlaces' page is requested (POST) with valid data
    THEN check that the club have enough points
    """

    CLUB_TO_TEST = 'She Lifts'
    COMPETITION_TO_TEST = 'Spring Festival'
    PLACES_TO_BUY = random.randint(1, 12)

    club = [c for c in clubs if c['name'] == CLUB_TO_TEST][0]
    competition = [comp for comp in competitions if comp['name'] == COMPETITION_TO_TEST][0]

    club_points_before = club['points']

    response = server.app.test_client().post(
        '/purchasePlaces', data=dict(
            club=CLUB_TO_TEST,
            competition=COMPETITION_TO_TEST,
            places=PLACES_TO_BUY
        ), follow_redirects=True)

    assert response.status_code == 200

    if (PLACES_TO_BUY > club_points_before):
        b"Sorry but this email does not exist" in response.data
