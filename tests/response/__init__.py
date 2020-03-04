import json
import os
import datetime


def load_file(filename: str) -> dict:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path, "resources", filename)
    with open(filepath, "r") as f:
        return json.loads(f.read())


def parse_time(time: str):
    dt = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    return dt.replace(tzinfo=datetime.timezone.utc)
