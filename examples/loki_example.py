import os
import time

import requests

USER_ID = os.getenv("LOKI_USER_ID")
API_KEY = os.getenv("LOKI_TOKEN")

logs = {
    "streams": [
        {
            "stream": {"Language": "Python", "source": "Code"},
            "values": [
                [
                    str(int(time.time()) * 1000000000),
                    "This is my log line",
                ]
            ],
        }
    ]
}


requests.post(
    url="https://logs-prod-024.grafana.net/loki/api/v1/push",
    auth=(USER_ID, API_KEY),
    json=logs,
    headers={"Content-Type": "application/json"},
)
