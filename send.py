import os

import requests

"""
Lazy quick test script
"""

PASSWORD = os.environ["GAEPROXY_PASSWORD"]


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

print(resp.text)
