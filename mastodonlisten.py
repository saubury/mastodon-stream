import mastodon
from mastodon import Mastodon
from bs4 import BeautifulSoup
import argparse
import datetime

from kafkaproducer import kafka_producer

# globals
base_url = ''
enable_kafka = False
quiet = False

# if enable_kafka:
topic_name, producer = kafka_producer()

#### Listener for Mastodon events

class Listener(mastodon.StreamListener):

    def on_update(self, status):
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

def main():
    global base_url
    global enable_kafka
    global quiet

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

    if args.public:
        mastodon.stream_public(Listener())
    else:
        mastodon.stream_local(Listener())

if __name__ == '__main__':
    main()
