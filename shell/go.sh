#!/bin/bash

BASE=/Users/simonaubury/git/saubury/mastodon-stream/
PY=./env/bin/python
cd ${BASE}

 

while true; do echo Start; ${PY} mastodonlisten.py --enableKafka --public; sleep 30; done &