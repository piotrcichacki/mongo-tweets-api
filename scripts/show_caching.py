import time

import requests
from redis.client import Redis
from requests import Response


def show_response(resp: Response) -> None:
    print(f"STATUS_CODE: {resp.status_code} \nBODY: {resp.json()} \nHEADERS: {resp.headers}\n")


def show_redis(r: Redis) -> None:
    print(f"REDIS KEYS: {r.keys()}\n")


if __name__ == "__main__":
    redis = Redis(host="localhost", port=6379)

    for _ in range(10):
        show_redis(redis)
        response = requests.get("http://localhost:8000/api/v1/tweets?limit=3")
        show_response(response)
        time.sleep(5)
