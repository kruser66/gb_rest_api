# REST_api for GB intership project 

RESTfull API for education project on Python 

## Getting Started

### Requirements

Python 3.5+
DB MySQL (local or remote)

### Installing
```
pip install -r requirements.txt
```

## How to use

### Config
Change config.py for setting up connect parameters to database

### Linux
```
$ gunicorn app:api -b 127.0.0.1:8000
$ curl http://localhost:8000/v1/users
```

### Windows
```
python run.py
in browser http://127.0.0.1:8000/v1
```
