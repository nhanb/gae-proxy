import os

import requests
from bottle import HTTPResponse, default_app, request, route, run

# GAE recommended
PORT = os.environ.get("PORT", 8080)
PASSWORD = os.environ.get("GAEPROXY_PASSWORD", "")

proxiable_methods = {
    "get": requests.get,
    "post": requests.post,
}


@route("/proxy", method="POST")
def proxy():
    req = request.json

    fields = ("method", "password", "url", "body")
    missing_fields = [f for f in fields if f not in req]
    if missing_fields:
        return HTTPResponse(status=400, body=f"Missing fields: {missing_fields}")

    if req["method"] not in proxiable_methods:
        return HTTPResponse(status=400, body="We serve get/post only!")

    if req.get("password") != PASSWORD:
        return HTTPResponse(status=400, body="Get off my lawn!")

    requests_func = proxiable_methods[req["method"]]
    requests_kwargs = {"url": req["url"], "headers": req["headers"]}
    if req["method"] == "post":
        requests_kwargs["body"] = req["body"]

    try:
        resp = requests_func(**requests_kwargs, timeout=10)
    except Exception as e:
        return HTTPResponse(status=500, body=f"Unexpected error:\n{e}")

    return HTTPResponse(body=resp.text, status=resp.status_code)


app = default_app()

if __name__ == "__main__":
    run(host="localhost", port=PORT)
