import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def go_to_index(self):
        self.client.get("/")


def on_start(self):
    self.client.post("/show-summary", {"email": "testuser@k.fr"})
