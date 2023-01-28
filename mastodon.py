# https://medium.com/@tspann/mastodon-streaming-to-pulsar-via-python-be7538112023

import mastodon
from mastodon import Mastodon
from bs4 import BeautifulSoup

#### Listener for Mastodon events

class Listener(mastodon.StreamListener):

    def on_update(self, status):

        if status.language in [ 'en', 'fr' ]: 
            # print('FOO ')

            m_text = BeautifulSoup(status.content, "html.parser").text

            print(f'status.language {status.language}', type(status.language))
            print(f'status.favourites_count {status.favourites_count}', type(status.favourites_count))
            print(f'status.account.username {status.account.username}', type(status.account.username))
            print(f'status.account.display_name {status.account.display_name}', type(status.account.display_name))
            print(f'status.account.bot {status.account.bot}', type(status.account.bot))
            print(f'status.tags {status.tags}', type(status.tags))
            num_tags = len(status.tags)
            num_chars = len(m_text)
            num_words = len(m_text.split())

            print(f'num_tags {num_tags}')
            print(f'num_chars {num_chars}')
            print(f'num_words {num_words}')
            print(m_text)
            print()
            print('*******************')
            exit


Mastodon.create_app(
    'streamreader',
    api_base_url = 'https://mastodon.social'
)

mastodon = Mastodon(api_base_url='https://mastodon.social')
mastodon.stream_public(Listener())