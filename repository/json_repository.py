import json

from model.warrior import Warrior


def read_json(path):
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return {}

def convert_to_warrior(json):
    return Warrior(
    id = json["id"],
    name = json["name"],
    ki = json["ki"],
    maxKi = json["maxKi"],
    race = json["race"],
    gender = json["gender"],
    description = json["description"],
    affiliation = json["affiliation"]
)

