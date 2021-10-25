from ...server import app


def test_login():
    """
    WHEN the '/show-summary' page is requested (POST) with an unknown email
    THEN check that the response is valid
    """

    with app.test_client() as test_client:
        response = test_client.post('/show-summary', data=dict(
            email="unknown-email97688@gmail.com"
        ), follow_redirects=True)

    assert response.status_code == 200
    assert b"Sorry but this email does not exist" in response.data
