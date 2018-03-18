from trakt.mapper.search import SearchMapper

import warnings
import requests


def query_with_genres(search_interface,
                      query, media=None, year=None, fields=None, genres=None, limit=None, extended=None, **kwargs):
    """Search by titles, descriptions, translated titles, aliases, and people.

    **Note:** Results are ordered by the most relevant score.

    :param search_interface: Trakt search interface
    :type query: :class:`SearchInterface`

    :param query: Search title or description
    :type query: :class:`~python:str`

    :param media: Desired media type (or :code:`None` to return all matching items)

        **Possible values:**
         - :code:`movie`
         - :code:`show`
         - :code:`episode`
         - :code:`person`
         - :code:`list`

    :type media: :class:`~python:str` or :class:`~python:list` of :class:`~python:str`

    :param year: Desired media year (or :code:`None` to return all matching items)
    :type year: :class:`~python:str` or :class:`~python:int`

    :param fields: Fields to search for :code:`query` (or :code:`None` to search all fields)
    :type fields: :class:`~python:str` or :class:`~python:list`

    :param genres: Desired media genres (or :code:`None` to return all matching items)
    :type fields: :class:`~python:str` or :class:`~python:list`

    :param extended: Level of information to include in response

        **Possible values:**
         - :code:`None`: Minimal (e.g. title, year, ids) **(default)**
         - :code:`full`: Complete

    :type extended: :class:`~python:str`

    :param kwargs: Extra request options
    :type kwargs: :class:`~python:dict`

    :return: Results
    :rtype: :class:`~python:list` of :class:`trakt.objects.media.Media`
    """
    # Validate parameters
    if not media:
        warnings.warn(
            "\"media\" parameter is now required on the Trakt['search'].query() method",
            DeprecationWarning, stacklevel=2
        )

    if fields and not media:
        raise ValueError('"fields" can only be used when the "media" parameter is defined')

    # Build query
    query = {
        'query': query
    }

    if year:
        query['year'] = year

    if fields:
        query['fields'] = fields

    if extended:
        query['extended'] = extended

    if genres:
        query['genres'] = genres

    if limit:
        query['limit'] = limit

    # Serialize media items
    if isinstance(media, list):
        media = ','.join(media)

    # Send request
    response = search_interface.http.get(
        params=[media],
        query=query
    )

    # Parse response
    items = search_interface.get_data(response, **kwargs)

    if isinstance(items, requests.Response):
        return items

    if items is not None:
        return SearchMapper.process_many(search_interface.client, items)

    return None
