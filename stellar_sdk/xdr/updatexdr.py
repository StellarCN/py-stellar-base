import os
from urllib.parse import urljoin

import requests

BASE_XDR_GITHUB_URL = (
    "https://raw.githubusercontent.com/stellar/stellar-core/master/src/xdr/"
)
XDR_FILES = (
    "Stellar-SCP.x",
    "Stellar-ledger-entries.x",
    "Stellar-ledger.x",
    "Stellar-overlay.x",
    "Stellar-transaction.x",
    "Stellar-types.x",
)
BASE_DIR = os.path.abspath(os.path.join(__file__, "../../../.xdr"))
print(f"Downloading xdr files from {BASE_XDR_GITHUB_URL}")
for filename in XDR_FILES:
    print(f"Downloading {filename}")
    url = urljoin(BASE_XDR_GITHUB_URL, filename)
    file = os.path.join(BASE_DIR, filename)
    resp = requests.get(url, allow_redirects=True)
    open(file, "wb").write(resp.content)
print("Finished")
