import random
from api_tv_shows import search_show, search_shows_by_genres
from data_access import insert_show, clear_table, get_all_shows


def setup_clear(alexa_id):
    clear_table(alexa_id)


def setup_one_show(alexa_id, show_name):
    show = search_show(show_name)
    if show:
        show_inserted = insert_show(alexa_id, __get_show_id(show), show.title)
        if show_inserted:
            genres_count = len(show.genres)
            if genres_count > 1:
                related = search_shows_by_genres(show.genres, 20)
                filter_related = __filter_shows(related, show.genres)
                for related_show in filter_related:
                    insert_show(alexa_id, __get_show_id(related_show), related_show.title)
        return show_inserted
    return None


def select_a_show(alexa_id):
    shows = get_all_shows(alexa_id)
    show = random.choice(shows)
    return show


def __filter_shows(shows, genres):
    filtered = []
    for show in shows:
        add = True
        for genre in genres:
            if genre not in show.genres:
                add = False
                break
        if add:
            filtered.append(show)
    return filtered


def __get_show_id(show):
    return int(show.keys[0][1])


def __setup_test():
    setup_clear('testid1')
    setup_one_show('testid1', 'Seinfeld')
    setup_one_show('testid1', 'Mr Robot')
    setup_one_show('testid1', 'The Walking Dead')
    setup_one_show('testid1', 'Game Of Thrones')
    return select_a_show('testid1')


