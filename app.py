"""
Dumb (bespoke "protocol" & grossly inefficient) http(s) proxy on Google Cloud Functions.
It also attempts to solve CloudFlare's javascript challenge where necessary.

To use, simply send request to proxy just as you would to the target, but provide some
extra http headers:

- X-Proxy-Key: For authentication.
- X-Proxy-Target-Host: So the proxy knows what hostname to proxy to.
- X-Proxy-Target-Scheme: Optional. Defaults to https.

To deploy:

    $ export GAEPROXY_KEY='my-secret-proxy-key'
    $ gcloud app deploy
"""

import os

import cloudscraper
from flask import Flask, Response, request

http = cloudscraper.create_scraper(
    browser={"browser": "firefox", "platform": "windows", "mobile": False}
)

PROXY_KEY = os.environ["GAEPROXY_KEY"]


app = Flask(__name__)


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def hello_world(path):
    auth_key = request.headers.get("X-Proxy-Key")
    if auth_key != PROXY_KEY:
        return "Go away", 403

    target_headers = {
        key: val
        for key, val in dict(request.headers).items()
        if not (
            key.startswith("X-Appengine-")
            or key
            in (
                "Accept-Encoding",
                "Content-Length",
                "Transfer-Encoding",
                "X-Amzn-Trace-Id",
                "X-Cloud-Trace-Context",
                "X-Forwarded-For",
                "X-Forwarded-Proto",
            )
        )
    }
    target_headers.pop("X-Proxy-Key")
    target_headers.pop("Host")

    target_host = target_headers.pop("X-Proxy-Target-Host")
    target_scheme = target_headers.pop("X-Proxy-Target-Scheme", "https")
    target_path = "/".join(request.full_path.split("/")[1:])
    target_url = f"{target_scheme}://{target_host}/{target_path}"

    post_form = {key: val for key, val in request.form.items()} or None

    send = getattr(http, request.method.lower())
    target_resp = send(target_url, headers=target_headers, data=post_form)

    resp_headers = dict(target_resp.headers)
    resp_headers.pop("Content-Encoding", None)
    resp_headers.pop("Transfer-Encoding", None)
    resp_headers.pop("content-encoding", None)
    resp_headers.pop("transfer-encoding", None)

    return Response(
        response=target_resp.content,
        status=target_resp.status_code,
        headers=resp_headers,
    )
