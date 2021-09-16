
import os
from pathlib import Path
from pathlib import Path
import os, json, pickle, requests



def read_key():
    # res_det = Path(".stellar_env").read_text()
    file_path = os.getcwd()
    file_details = open(os.path.join(file_path, ".stellar_env"), mode="r", encoding="utf-8")
    res_det = file_details.read()
    user_my_details = json.loads(res_det)
    return user_my_details


