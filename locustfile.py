import uuid

from locust import HttpUser, task

class WebhookEvent(HttpUser):
    @task
    def webhook_transfer(self):
        json = {
            "transfer_id": str(uuid.uuid4()),
            "transfer_date": "2025-03-07",
            "value": 253401,
            "origin": "Locust",
            "status": "CREATED"
        }
        self.client.post("/webhook/transfers", json=json)
