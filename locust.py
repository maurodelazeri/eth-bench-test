from locust import HttpUser, TaskSet, task, between
import json
import random
import sys
import random

headers = {
    'Content-Type': 'application/json',
}

eth_getTransactionReceipt = open("eth_getTransactionReceipt.json").readlines()

def run_request(locust, data, name):
    data["id"] = random.randint(0, sys.maxsize)
    with locust.client.post("", name=name, json=data, catch_response=True) as response:
        try:
            data = json.loads(response.content)
        except json.decoder.JSONDecodeError:
            response.failure("Invalid JSON")
        else:
            if data.get("error", False):
                response.failure("Payload error: %s" % data.get("error"))
            elif data.get("id") != data["id"]:
                response.failure("Mismatched IDs")
            else: response.success()
        return response

class RunFullTest(TaskSet):
    @task()
    def eth_getTransactionReceipt(locust):
        randon_json=random.choice(eth_getTransactionReceipt)
        data = json.loads(randon_json)
        run_request(locust,  data, name="eth_getTransactionReceipt")


class WebsiteUser(HttpUser):
    tasks = [RunFullTest]
    wait_time = between(1, 5)
