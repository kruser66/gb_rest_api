from api import *
from waitress import serve


serve(api, host='gbdb', port=8000)