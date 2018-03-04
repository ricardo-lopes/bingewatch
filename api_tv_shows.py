from trakt import Trakt
import os


def __login():
    Trakt.configuration.defaults.client(
        id=os.environ['TRAKTID'],
        secret=os.environ['TRAKTSECRET']
    )


def search_show(show_name):
    __login()
    shows = Trakt['search'].query(show_name, 'show', extended='full')
    if shows:
        return shows[0]
    return None

