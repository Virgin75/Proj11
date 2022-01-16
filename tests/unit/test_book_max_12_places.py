from ...server import app
from ...db import update_club_points, update_competition_places, clubs, competitions


def test_book_max_12_places():
    """
    WHEN the '/purchasePlaces' page is requested (POST) with more than 12 places to book
    THEN there should be an error because this is too much
    """
    CLUB_TO_TEST = 'She Lifts'
    COMPETITION_TO_TEST = 'Spring Festival'
    PLACES_TO_BUY = 13

    # Make sure the test club has enough points for this test // Same for the competition
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
    print(clubs)
    print(response.data)
    assert b"You are not allowed to book more than 12 places" in response.data
