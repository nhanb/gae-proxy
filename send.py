import requests

"""
Lazy quick test script
"""

resp = requests.post(
    "http://localhost:8080/proxy",
    json={
        "url": "https://httpbin.org/get",
        "method": "get",
        "body": None,
        "headers": {"Foo-Bar": "ehhhh"},
    },
)

print(resp.status_code)
for hkey, hval in resp.headers.items():
    print(hkey, ":", hval)

print(resp.text)
