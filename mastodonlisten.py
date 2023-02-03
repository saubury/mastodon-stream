import mastodon
from mastodon import Mastodon
from bs4 import BeautifulSoup
import argparse
import datetime
from threading import Timer
import os

from kafkaproducer import kafka_producer

# globals
base_url = ''
enable_kafka = False
quiet = False
watchdog = False

if enable_kafka:
    topic_name, producer = kafka_producer()
else:
    topic_name, producer = '' , ''


# Listener for Mastodon events
class Listener(mastodon.StreamListener):

    def on_update(self, status):
        if watchdog:
            # reset watchdog timer
            watchdog.reset()

        m_text = BeautifulSoup(status.content, 'html.parser').text
        num_tags = len(status.tags)
        num_chars = len(m_text)
        num_words = len(m_text.split())
        m_lang = status.language
        if m_lang is None:
            m_lang = 'unknown'
        m_user = status.account.username

        app=''
        # attribute only available on local
        if hasattr(status, 'application'):
            app = status.application.get('name')
        
        value_dict = { 
            'm_id': status.id,
            'created_at': int(datetime.datetime.now().strftime('%s')),
            'app': app,
            'url': status.url,
            'base_url': base_url,  
            'language': m_lang, 
            'favourites': status.favourites_count, 
            'username': m_user, 
            'bot': status.account.bot, 
            'tags': num_tags, 
            'characters': num_chars, 
            'words': num_words, 
            'mastodon_text': m_text
        }

        if not quiet:
            print(f'{m_user} {m_lang}', m_text[:30])


        if enable_kafka:
            producer.produce(topic = topic_name, value = value_dict)
            producer.flush()


class Watchdog:
    def __init__(self, timeout, userHandler=None): # timeout in seconds
        self.timeout = timeout
        if userHandler != None:
            self.timer = Timer(self.timeout, userHandler)
        else:
            self.timer = Timer(self.timeout, self.handler)

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, watchExpired)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def handler(self):
        raise self;


def watchExpired():
    print('Watchdog expired')
    # ugly, but expected method for a child process to terminate a fork
    os._exit(1)


def main():
    global base_url
    global enable_kafka
    global quiet
    global watchdog

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '--enableKafka',
        help='Whether to enable Kafka producer.',
        action='store_true',
        required=False,
        default=False)

    parser.add_argument(
        '--public',
        help='listen to public stream (instead of local).',
        action='store_true',
        required=False,
        default=False)

    parser.add_argument(
        '--watchdog',
        help='enable watchdog timer of n seconds',
        type=int,
        required=False)

    parser.add_argument(
        '--quiet',
        help='Do not echo a summary of the toot',
        action='store_true',
        required=False,
        default=False)

    parser.add_argument(
        '--baseURL',
        help='Server URL',
        required=False,
        default='https://mastodon.social')      

    args = parser.parse_args()

    base_url=args.baseURL
    enable_kafka=args.enableKafka
    mastodon = Mastodon(api_base_url = base_url)

    if args.watchdog:
        watchdog = Watchdog(args.watchdog, watchExpired)
        watchdog.timer.start()

    if args.public:
        mastodon.stream_public(Listener())
    else:
        mastodon.stream_local(Listener())

if __name__ == '__main__':
    main()
