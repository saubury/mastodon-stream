#!/bin/bash

BASE=${HOME}/git/saubury/mastodon-stream/
PY=./env/bin/python
cd ${BASE}

 

# while true; do echo Start; ${PY} mastodonlisten.py --enableKafka --public; sleep 30; done &

while true; do echo Start; ${PY} mastodonlisten.py --baseURL https://mastodon.social       --enableKafka --public; sleep 30; done
while true; do echo Start; ${PY} mastodonlisten.py --baseURL https://hachyderm.io          --enableKafka ; sleep 30; done
while true; do echo Start; ${PY} mastodonlisten.py --baseURL https://mastodon.au/          --enableKafka ; sleep 30; done
while true; do echo Start; ${PY} mastodonlisten.py --baseURL https://data-folks.masto.host --enableKafka ; sleep 30; done

