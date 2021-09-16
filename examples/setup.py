"""
1. Create a .secrets file
2. Create a keypair
3. add created keypair secret to the .secret file
4. make it load to all transactions



"""

# Path(os.path.join(dir_link, "Bridges/.distributor")).read_text()
import os, json, pickle, requests
from stellar_sdk.keypair import Keypair



class SetUp:
    all_keys ={}

    def __init__(self) -> None:
        self.setup()

    def key_pairs(self, *args) -> str: #Create Random Keypair
        keys = Keypair.random()
        return keys.secret



    def setup(self):
        adc = map(self.key_pairs, [1,2,3,4,5])
        _list_adc = list(adc)
        for i in range(len(_list_adc)):
            #Getting Testnet Lumen
            url = "https://friendbot.stellar.org"
            response = requests.get(url, params={"addr": Keypair.from_secret(_list_adc[i]).public_key})
            if response.status_code == 200:

                #Write secret key to File
                self.all_keys['source_key_'+str(i)] = _list_adc[i]
                print(f"{self.all_keys['source_key_'+ str(i)]}" + " funded")
                file_path = os.getcwd()
                my_file = open(os.path.join(file_path, ".stellar_env"), mode="w+", encoding="utf-8")
                before_write = json.dumps(self.all_keys, indent=4)
                my_file.write(before_write)
                my_file.close()
            else:
                print("Something went wrong")




if __name__ == "__main__":
    SetUp()

# print(all_keys)
# print(all_keys['source_key'])
