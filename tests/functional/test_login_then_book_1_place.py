from ...server import app
from ...db import clubs, competitions


def test_login_then_book_one_place():
    """
    Test if I can log in, see user info correctly then 
    book 1 place in the first competition.
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

    # Book a place in first available competition in the list
    raw = str(response.data)
    href = '<a href="'
    fin = '">Book Places'

    # Finding href link in page to book a meeting
    start = -1
    for i in range(0, 2):
        start = raw.find(href, start + 1)
    end = -1
    for i in range(0, 1):
        end = raw.find(fin, end + 1)

    book_link = raw[start:end][9:]

    with app.test_client() as test_client:
        book_response = test_client.get(book_link)

    # Book 1 place if the tested club has more than 3 pts left
    get_comp_from_url = book_link[6:]
    slash_indx = get_comp_from_url.find('/')

    CURRENT_COMPETITION = get_comp_from_url[:slash_indx]
    POINTS_AVAILABLE = clubs[1]['points']

    if POINTS_AVAILABLE >= 3:
        with app.test_client() as test_client:
            final_response = test_client.post('/purchasePlaces', data=dict(
                club=clubs[1]['name'],
                competition=CURRENT_COMPETITION.replace('%20', ' '),
                places=1
            ))

    assert b"Great-booking complete!" in final_response.data
