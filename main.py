import requests
from bottle import HTTPResponse, request, route, run

proxiable_methods = {
    "get": requests.get,
    "post": requests.post,
}


@route("/proxy", method="POST")
def proxy():
    req = request.json
    assert req["method"] in proxiable_methods
    requests_func = proxiable_methods[req["method"]]
    requests_kwargs = {"url": req["url"], "headers": req["headers"]}
    if req["method"] == "post":
        requests_kwargs["body"] = req["body"]

    try:
        resp = requests_func(**requests_kwargs, timeout=10)
    except Exception as e:
        return HTTPResponse(status=500, body=f"Unexpected error:\n{e}")

    return HTTPResponse(body=resp.text, status=resp.status_code)


run(host="0.0.0.0", port=8080)
