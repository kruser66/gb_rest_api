from api import *
from waitress import serve

from models import *
from playhouse.shortcuts import model_to_dict
import json


prs = Personspagerank.select()
print(json.dumps([model_to_dict(p) for p in prs]))


serve(api, host='127.0.0.1', port=8000)