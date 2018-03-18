from trakt import Trakt
import os

from trakt_extension import query_with_genres


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


def search_shows_by_genres(genres, results_limit):
    __login()
    search_interface = Trakt['search']
    shows = query_with_genres(search_interface, '', 'show', genres=genres, limit=results_limit, extended='full')
    if shows:
        return shows
    return None


