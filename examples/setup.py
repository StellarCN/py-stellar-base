"""
1. Create a .secrets file
2. Create a keypair
3. add created keypair secret to the .secret file
4. make it load to all transactions

--- Should create destination account too
--- Create a default Asset Code and Asset Issuer

"""

# Path(os.path.join(dir_link, "Bridges/.distributor")).read_text()
import os, json, pickle, requests
from stellar_sdk.keypair import Keypair



class SetUp:
    all_keys ={}

    def __init__(self, num : int) -> None:
        self.acct_num = num
        self.setup()

    def key_pairs(self, *args) -> str: #Create Random Keypair
        keys = Keypair.random()
        return keys

    def friendBot(self, secret_ket :str) -> str:
        url = "https://friendbot.stellar.org"
        response = requests.get(url, params={"addr": Keypair.from_secret(secret_ket).public_key})
        return response



    def setup(self):

        for i in range(self.acct_num):
            #generate rnadom keypair
            source_key = self.key_pairs()

            #Getting Testnet Lumen
            resp = self.friendBot(source_key.secret)

            if resp.status_code == 200:
                #Write secret key to File
                self.all_keys['source_key_'+str(i)] = source_key.secret
                print(f"{self.all_keys['source_key_'+ str(i)]}" + " funded")

            else:
                print("Something went wrong")

        for i in range(self.acct_num):
            destination_acct = self.key_pairs()

            #Getting Testnet Lumen
            resp = self.friendBot(destination_acct.secret)
            if resp.status_code == 200:
                self.all_keys.update({
                    f"{'destination_acct_'+str(i)}": destination_acct.public_key
                })

                print(f"{self.all_keys['destination_acct_'+ str(i)]}" + " funded")

            else:
                print("Something went wrong")

        file_path = os.getcwd()
        my_file = open(os.path.join(file_path, ".stellar_env"), mode="w+", encoding="utf-8")
        before_write = json.dumps(self.all_keys, indent=4)
        my_file.write(before_write)
        my_file.close()





if __name__ == "__main__":
    # SetUp()
    acct = input("Total Number of Source Account and Destination Account You will like to Create? ")
    if acct:
        SetUp(int(acct))

    else:
        SetUp(5)

# print(all_keys)
# print(all_keys['source_key'])
