from python:3
copy . /app
workdir /app
run pip install -r requirements/requirements.txt
cmd python groupchat.py
