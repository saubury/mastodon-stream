# https://medium.com/@tspann/mastodon-streaming-to-pulsar-via-python-be7538112023

import mastodon
from mastodon import Mastodon
from bs4 import BeautifulSoup

from kafkaproducer import kafka_producer

topic_name, producer = kafka_producer()

#### Listener for Mastodon events

class Listener(mastodon.StreamListener):

    def on_update(self, status):
        if status.language in [ 'en', 'fr' ]: 
            m_text = BeautifulSoup(status.content, "html.parser").text
            num_tags = len(status.tags)
            num_chars = len(m_text)
            num_words = len(m_text.split())
            print(m_text)

            value_dict = {  "language": status.language, "favourites": status.favourites_count, "username": status.account.username, "bot": status.account.bot, "tags": num_tags, "characters": num_chars, "words": num_words}
            producer.produce(topic = topic_name, value = value_dict)
            producer.flush()


def main():
    mastodon = Mastodon(api_base_url='https://mastodon.social')
    mastodon.stream_public(Listener())

if __name__ == "__main__":
    main()
