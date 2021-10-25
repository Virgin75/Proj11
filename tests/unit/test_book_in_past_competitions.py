from ...server import app
from ...db import competitions, clubs
from datetime import datetime

from ...db import update_club_points, update_competition_places


def test_book_in_past_competitions():
    """
    WHEN the '/purchasePlaces' page is requested (POST) with data
      containing a competition date that is in the past
    THEN there should be an error.
    """
    CLUB_TO_TEST = 'She Lifts'
    COMPETITION_TO_TEST = next(comp for comp in competitions
                               if datetime.strptime(comp['date'], "%Y-%m-%d %H:%M:%S") < datetime.now())['name']
    PLACES_TO_BUY = 1

    update_club_points(next(i for i, club in enumerate(clubs)
                            if club["name"] == CLUB_TO_TEST), 15)
    update_competition_places(next(i for i, comp in enumerate(competitions)
                                   if comp["name"] == COMPETITION_TO_TEST), 14)

    with app.test_client() as test_client:
        response = test_client.post('/purchasePlaces', data=dict(
            club=CLUB_TO_TEST,
            competition=COMPETITION_TO_TEST,
            places=PLACES_TO_BUY
        ))

    assert response.status_code == 200
    assert b"This event is over. You cannot book a place anymore." in response.data
