from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)  # Wait between 1 and 2 seconds between tasks

    @task
    def load_data(self):
        self.client.get("/data/", name="Get data")
