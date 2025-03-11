import uuid
from datetime import date
import random

from locust import HttpUser, task, between, SequentialTaskSet


class UserTasks(SequentialTaskSet):
    @task
    def webhook_transfer_created(self):
        transfer_id = str(uuid.uuid4())

        json = {
            "transfer_id": transfer_id,
            "transfer_date": date.today().isoformat(),
            "value": random.randint(10000, 100000),
            "origin": "Locust",
            "status": "CREATED"
        }
        with self.client.post("/webhook/transfers", json=json) as response:
            if response.status_code == 200:
                self.user.transfer_id = transfer_id

    @task
    def webhook_transfer_updated(self):
        transfer_id = self.user.context()["transfer_id"]

        json = {
            "transfer_id": transfer_id,
            "transfer_date": date.today().isoformat(),
            "value": random.randint(10000, 100000),
            "origin": "Locust",
            "status": "UPDATED"
        }
        self.client.post("/webhook/transfers", json=json)

    @task
    def webhook_transfer_complete(self):
        transfer_id = self.user.context()["transfer_id"]

        json = {
            "transfer_id": transfer_id,
            "status": "COMPLETED"
        }
        self.client.post("/webhook/transfers", json=json)

class WebhookEvent(HttpUser):
    wait_time = between(1, 5)
    tasks = [UserTasks]

    def on_start(self) -> None:
        self.transfer_id = None

    def context(self):
        return {"transfer_id": self.transfer_id}
