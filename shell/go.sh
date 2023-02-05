#!/bin/bash

BASE=${HOME}/git/saubury/mastodon-stream/
PY=./env/bin/python
cd ${BASE}

 

# while true; do echo Start; ${PY} mastodonlisten.py --enableKafka --public; sleep 30; done &

while true; do echo Start; ${PY} mastodonlisten.py --baseURL https://mastodon.social       --enableKafka --watchdog 30 --public; sleep 30; done
while true; do echo Start; ${PY} mastodonlisten.py --baseURL https://hachyderm.io          --enableKafka --watchdog 30 ; sleep 30; done
while true; do echo Start; ${PY} mastodonlisten.py --baseURL https://mastodon.au/          --enableKafka --watchdog 30 ; sleep 30; done
while true; do echo Start; ${PY} mastodonlisten.py --baseURL https://data-folks.masto.host --enableKafka --watchdog 30 ; sleep 30; done

