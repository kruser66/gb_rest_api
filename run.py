from api import *
from waitress import serve

# import datetime
#
# from models import *
# from playhouse.shortcuts import model_to_dict
# import json
#
#
# prs = Pages.get(Pages.id == 1)
#
# now = datetime.datetime.now()
# frombase = datetime.datetime.strptime(prs.foundDateTime, '%Y-%m-%d %H:%M:%S')
# print(now.date() < frombase.date())
#
#
# print(json.dumps([model_to_dict(p) for p in prs]))


serve(api, host='127.0.0.1', port=8000)