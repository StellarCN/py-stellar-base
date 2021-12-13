import os
from typing import List

import requests

from stellar_sdk import Keypair

base_dir = os.path.dirname(os.path.realpath(__file__))


def active_account(*accounts: List[str]):
    url = "https://friendbot.stellar.org"
    for account in accounts:
        response = requests.get(url, params={"addr": account})
        if response.status_code != 200:
            # TODO: raise error
            pass


def init_account_merge_py():
    # account_merge.py
    account_merge_py_path = os.path.join(base_dir, "account_merge.py")
    kp1, kp2 = Keypair.random(), Keypair.random()
    active_account(kp1.public_key, kp2.public_key)

    with open(account_merge_py_path, 'r') as f:
        content = f.read()

    content = content.replace("SC7AUS23UKVZQL5KMIK4ZK3EZJUS6ZVMTQSVLH3VIK42W6RBQAQXOVQX", kp1.secret)
    content = content.replace("GANXMF6DCQNHZP5ULDONM4VNXBV5YECTDGLGXCESXNT66H6AZSAHLFGK", kp2.public_key)

    with open(account_merge_py_path, 'w') as f:
        f.write(str(content))


# build_fee_bump_transaction.py
# TODO...

if __name__ == '__main__':
    print("initialize...")
    init_account_merge_py()
    print("done")
