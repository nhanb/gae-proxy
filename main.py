import os

import requests
from bottle import HTTPResponse, request, route, run

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

    if req["method"] not in proxiable_methods:
        return HTTPResponse(status=400, body="We serve get/post only!")

    if req["password"] != PASSWORD:
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


run(host="0.0.0.0", port=PORT)
