import os
from datetime import datetime as dt

import requests

"""
Lazy quick test script
"""

PASSWORD = os.environ["GAEPROXY_PASSWORD"]

while True:
    start = dt.now()
    resp = requests.post(
        "https://nhansproxy.df.r.appspot.com/proxy",
        json={
            "url": "https://httpbin.org/ip",
            "method": "get",
            "body": None,
            "headers": {"Foo-Bar": "ehhhh"},
            "password": PASSWORD,
        },
    )

    """
    print(resp.status_code)
    for hkey, hval in resp.headers.items():
        print(hkey, ":", hval)
    """
    end = dt.now()
    print(resp.status_code)
    print((end - start).total_seconds())
