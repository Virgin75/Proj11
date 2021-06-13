from pythontesting import server


def test_login():
    """
    GIVEN a Flask application.
    WHEN the '/show-summary' page is requested (POST) with an unknown email
    THEN check that the response is valid
    """
    response = server.app.test_client().post(
        '/show-summary', data=dict(
            email="unknown-email@gmail.com"
        ), follow_redirects=True)

    assert response.status_code == 200
    assert b"Sorry but this email does not exist" in response.data
