from api import *
from waitress import serve


serve(api, host='127.0.0.1', port=8000)