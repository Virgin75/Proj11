from ...server import app
from ...db import clubs, competitions


def test_login_then_logout():
    """
    Test if I can log in, see user info correctly then 
    log out and being redirected to the correct page.
    """

    AUTHORIZED_EMAILS = [club['email'] for club in clubs]
    COMPETITIONS_NAMES = [comp['name'] for comp in competitions]

    with app.test_client() as test_client:
        response = test_client.post('/show-summary', data=dict(
            email=AUTHORIZED_EMAILS[1]
        ), follow_redirects=True)

    assert response.status_code == 200
    # User is logged in
    assert f"Welcome, {AUTHORIZED_EMAILS[1]}".encode() in response.data
    # Available competitions are displayed
    for comp in COMPETITIONS_NAMES:
        assert f"{comp}".encode() in response.data

    # User has logged out
    with app.test_client() as test_client:
        response_logout = test_client.get('/logout')

    assert response_logout.status_code == 302
    assert f"{AUTHORIZED_EMAILS[1]}".encode() not in response_logout.data
