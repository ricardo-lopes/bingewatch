import random
from api_tv_shows import search_show
from data_access import insert_show, clear_table, get_all_shows


def setup_one_show(alexa_id, show_id, show_name):
    show = search_show(show_name)
    if show:
        return insert_show(alexa_id, show_id, show.title)
    return None


def select_a_show(alexa_id):
    shows = get_all_shows(alexa_id)
    show = random.choice(shows)
    return show


def __setup_test():
    clear_table('testid1')
    setup_one_show('testid1', 1, 'Mr Robot')
    setup_one_show('testid1', 2, 'Seinfeld')
    setup_one_show('testid1', 3, 'The Walking Dead')
    setup_one_show('testid1', 4, 'Game Of Thrones')

