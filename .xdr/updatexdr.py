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
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
print("Downloading xdr files from {}".format(BASE_XDR_GITHUB_URL))
for filename in XDR_FILES:
    print("Downloading {}".format(filename))
    url = urljoin(BASE_XDR_GITHUB_URL, filename)
    file = os.path.join(BASE_DIR, filename)
    resp = requests.get(url, allow_redirects=True)
    open(file, "wb").write(resp.content)
print("Finished")
