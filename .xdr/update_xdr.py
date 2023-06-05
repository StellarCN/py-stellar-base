import os

import requests

REPO = "stellar/stellar-xdr"
BRANCH = "next"
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

print(f"Downloading xdr files from {REPO}")

raw_data = requests.get(
    f"https://api.github.com/repos/{REPO}/contents", params={"ref": BRANCH}
)
files = raw_data.json()

for file in files:
    filename: str = file["name"]
    if not filename.endswith(".x"):
        continue
    print(f"Downloading {filename}")
    download_url: str = file["download_url"]
    file = os.path.join(BASE_DIR, filename)
    resp = requests.get(download_url, allow_redirects=True)
    open(file, "wb").write(resp.content)
print("Finished")
