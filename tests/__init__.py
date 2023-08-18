import os

HTTPBIN_URL = "https://httpbin.org/"
if os.getenv("GITHUB_ACTIONS"):
    print("Running on Github Actions")
    HTTPBIN_URL = "http://127.0.0.1:9876/"
