"""
==============================================================
Example: Creating and Funding a Stellar Account using Python SDK
==============================================================

This example demonstrates how to create a new Stellar account and fund it
with a specified starting balance using the Stellar Testnet.

Operations performed:
1. Load an existing source account (already funded).
2. Generate a new random destination keypair.
3. Build a `Create Account` transaction to fund the new account.
4. Sign and submit the transaction.
5. Print transaction hash and new account credentials.

Official Documentation:
- Create Account: https://developers.stellar.org/docs/tutorials/create-account/#create-account
- List of operations: https://developers.stellar.org/docs/start/list-of-operations/#create-account
"""

# ==============================================================
# === Installation Guideline ===================================
# ==============================================================
# To run this example, you need to install the Stellar SDK for Python:
#
#     pip install stellar-sdk
#
# Save this script as `create_account.py` and run with:
#
#     python create_account.py
#
# ==============================================================
# === Import Required Libraries =================================
# ==============================================================

from stellar_sdk import Keypair, Network, Server, TransactionBuilder

# ==============================================================
# === 1. Setup Server and Source Account =======================
# ==============================================================

# Connect to the Stellar Testnet Horizon server
server = Server(horizon_url="https://horizon-testnet.stellar.org")

# Load an existing account that will fund the new account
# Replace this secret with your own testnet secret key
source = Keypair.from_secret("SBFZCHU5645DOKRWYBXVOXY2ELGJKFRX6VGGPRYUWHQ7PMXXJNDZFMKD")

# ==============================================================
# === 2. Generate a New Random Keypair for Destination =========
# ==============================================================

# Create a new random keypair for the account to be created
destination = Keypair.random()

# ==============================================================
# === 3. Load Source Account Details ===========================
# ==============================================================

# Load the source account from the Testnet Horizon server
source_account = server.load_account(account_id=source.public_key)

# ==============================================================
# === 4. Build Create Account Transaction ======================
# ==============================================================

# Build a transaction to create a new account
# and fund it with the starting balance of 12.25 XLM
transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,  # set fee per operation in stroops (0.00001 XLM)
    )
    .append_create_account_op(
        destination=destination.public_key,
        starting_balance="12.25",  # fund with 12.25 XLM
    )
    .set_timeout(30)  # transaction will timeout in 30 seconds
    .build()
)

# ==============================================================
# === 5. Sign and Submit Transaction ==========================
# ==============================================================

# Sign the transaction with the source account's secret key
transaction.sign(source)

# Submit the transaction to the Testnet
response = server.submit_transaction(transaction)

# ==============================================================
# === 6. Output Transaction and Account Details ==============
# ==============================================================

print(f"Transaction hash: {response['hash']}")
print(
    f"New Keypair: \n\taccount id: {destination.public_key}\n\tsecret seed: {destination.secret}"
)

# ==============================================================
# === Expected Output =========================================
# ==============================================================
# Example output (hash and keys will differ every run):
#
# Transaction hash: 70e023123fbf8b417ecea5ed923484e8d200beb792995d73d7692ab0875843b2
# New Keypair:
#       account id: GAPASWTZYIM2JZE5QLGID52PVD4QWCLCQLXWDSL7AA4ECES23WZGHMR4
#       secret seed: SB2TJS54Y2J52G5XVRJZLARUMYKSGAGQIG3NTWLR6SRY3MDQMGZUWJI2
#
# The new account has been created on the Stellar Testnet and funded
# with the starting balance specified.
# -----------------------------------------------------------------
