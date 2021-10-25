from ...server import app


def test_feature_points_display_board():
    """
    WHEN someone logs in to the app
    THEN they should be able to see the table of points of all teams
    """

    EMAIL_TO_TEST = 'admin@irontemple.com'

    with app.test_client() as test_client:
        response = test_client.post('/show-summary', data=dict(
            email=EMAIL_TO_TEST
        ))

    assert response.status_code == 200
    assert b'<table id="points_all_team">' in response.data
