import json
from pprint import pprint

import typer
import requests
from postmanparser import Collection

app = typer.Typer()


@app.command()
def run_presentation():
    some = create_request_collection()
    headers = None
    for i, request in enumerate(some[:2]):
        _, response, _ = make_request(headers, request)
        is_auth_request: bool = i == 1
        if is_auth_request:
            headers = extract_token(response)

    for request in some[2:]:
        make_request_with_pauses(headers, request)
        if request.url.raw == 'http://localhost:8082/join/1':
            make_request(headers, request)


def create_request_collection():
    collection = Collection()
    collection.parse_from_file("OralPresentation.postman_collection.json")
    some = collection.get_requests()
    return some


def extract_token(response):
    data = response.json()
    token = data['token']
    headers = {"Authorization": "Bearer " + token}
    return headers


def make_request_with_pauses(headers, request):
    data, response, url = make_request(headers, request)
    print(url)
    input()
    pprint(data)
    input()
    pprint(response.text)
    input()


def make_request(headers, request):
    url: str = request.url.raw
    data = json.loads(request.body.raw) if request.body else ''
    response = None
    match request.method:
        case 'PUT':
            response = requests.put(url, json=data, headers=headers)
        case 'POST':
            response = requests.post(url, json=data, headers=headers)
        case 'GET':
            response = requests.get(url, json=data, headers=headers)
    return data, response, url


if __name__ == '__main__':
    app()
