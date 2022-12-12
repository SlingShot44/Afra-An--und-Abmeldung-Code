import json
import os

def house_dict() -> dict[str,bool]:
    path = os.path.join(os.path.dirname(__file__),"..","config","locations.json")
    with open(path, encoding="UTF-8") as f:
        locations_dict = json.load(f)
        f.close()
    return locations_dict

def house_list() -> list[str]:
    locations_dict = house_dict()
    return [key for key in locations_dict]

def house_choices() -> list[tuple[int,str]]:
    locations_dict = house_dict()
    locations_list = house_list()
    return [(index, value) for index, value in enumerate(locations_list) if locations_dict[value]]

def houses_config() -> dict:
    path = os.path.join(os.path.dirname(__file__),"..","config","houses.json")
    with open(path, encoding="UTF-8") as f:
        house_conf = json.load(f)
        f.close()
    return house_conf