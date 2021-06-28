"""
This example shows how to activate an account via friendbot in a test network.

This feature is only available for test networks.

See: https://developers.stellar.org/docs/tutorials/create-account/#create-account
"""
import requests

from stellar_sdk import Keypair

keypair = Keypair.random()

print("Public Key: " + keypair.public_key)
print("Secret Seed: " + keypair.secret)

url = "https://friendbot.stellar.org"
response = requests.get(url, params={"addr": keypair.public_key})
print(response)
