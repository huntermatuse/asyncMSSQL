from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    # Base URL for all requests
    host = "http://172.16.111.34:8000"

    # Wait between 1 and 2 seconds between tasks
    wait_time = between(1, 2)

    @task
    def load_data(self):
        # Perform a GET request to the /data/ endpoint
        with self.client.get("/data/", name="Get data", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    # Try to parse the JSON response
                    data = response.json()
                    # Optionally, perform further checks or processing on 'data'
                except ValueError:
                    # Not a JSON response, or JSON is invalid
                    response.failure("Response was not valid JSON")
            else:
                # Report a non-200 status code as a failure
                response.failure(f"Unexpected status code: {response.status_code}")

