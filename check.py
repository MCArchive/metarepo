import yaml
import json
import os
import re
from schema import And, Use, Schema, Optional, Regex

mod_schema = Schema({
    'format': lambda x: x == 1,
    'name': str,
    'authors': [str],
    Optional('desc'): str,
    'versions': [{
        'name': str,
        Optional('desc'): str,
        'mcvsn': [str],
        'files': [{
            'filename': str,
            'ipfs': str,
            Optional('desc'): str,
            'hash': {
                'type': lambda x: x == "sha256",
                'digest': Regex(r'^[a-f0-9]{64}$', flags=re.I)
                },
            Optional('urls'): [{
                'type': lambda x: x == "original" or x == "page",
                'url': str
                }]
            }]
        }]
    })

for file_name in os.listdir("mods"):
    file = open("mods/" + file_name)
    if file_name.endswith(".json"):
        data = json.load(file)
    elif file_name.endswith(".yaml") or file_name.endswith(".yml"):
        data = yaml.load(file)
    Regex(r'^[a-z-_0-9.]*$').validate(file_name)
    mod_schema.validate(data)
