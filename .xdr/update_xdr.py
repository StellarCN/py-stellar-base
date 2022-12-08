import os
from urllib.parse import urljoin

import requests

BASE_XDR_GITHUB_URL = (
    "https://raw.githubusercontent.com/stellar/stellar-xdr/next/"
)
XDR_FILES = (
    "Stellar-contract-spec.x", "Stellar-ledger-entries.x", "Stellar-transaction.x",
    "Stellar-SCP.x", "Stellar-contract.x", "Stellar-ledger.x", "Stellar-types.x",
    "Stellar-contract-env-meta.x", "Stellar-internal.x", "Stellar-overlay.x"
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
