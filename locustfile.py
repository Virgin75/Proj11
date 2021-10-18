from locust import HttpUser, task


class QuickstartUser(HttpUser):

    @task
    def go_to_a_booking_page(self):
        self.client.get("/book/Spring%20Festival/Iron%20Temple")

    @task
    def book_a_place(self):
        self.client.post("/purchasePlaces", {"club": "Iron Temple",
                                             "competition": "Spring Festival",
                                             "places": 1})


def on_start(self):
    self.client.post("/show-summary", {"email": "admin@irontemple.com"})
