from boto3 import resource
from boto3.dynamodb.conditions import Key


def insert_show(alexaid, id, show_name):
    table = __get_shows_table()
    show = {
        "alexa_id": alexaid,
        "id": id,
        "title": show_name
    }
    return table.put_item(Item=show)


def insert_suggestion(alexaid, id, show_name):
    table = __get_suggestions_table()
    show = {
        "alexa_id": alexaid,
        "id": id,
        "title": show_name
    }
    return table.put_item(Item=show)


def clear_user_data(alexaid):
    suggestions_table = __get_suggestions_table()
    suggestions = get_all_suggestions(alexaid)
    __delete_table_contents(suggestions, suggestions_table)
    shows_table = __get_shows_table()
    shows = __get_all_shows(alexaid)
    __delete_table_contents(shows, shows_table)


def get_all_suggestions(alexaid):
    table = __get_suggestions_table()
    response = table.scan(
        FilterExpression=Key('alexa_id').eq(alexaid)
    )
    if response['Items']:
        return response['Items']
    return None


def __get_database():
    return resource('dynamodb', region_name='eu-west-1')


def __get_shows_table():
    return __get_database().Table('tvshows')


def __get_suggestions_table():
    return __get_database().Table('tvsuggestions')


def __get_all_shows(alexaid):
    table = __get_shows_table()
    response = table.scan(
        FilterExpression=Key('alexa_id').eq(alexaid)
    )
    if response['Items']:
        return response['Items']
    return None


def __delete_table_contents(rows, table):
    if rows:
        with table.batch_writer() as batch:
            for s in rows:
                batch.delete_item(
                    Key={
                        'alexa_id': s['alexa_id'],
                        'id': s['id']
                    }
                )


def __create_shows_table():
    db = __get_database()
    result = db.create_table(
        TableName='tvshows',
        KeySchema=[
            {
                'AttributeName': 'alexa_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'id',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'alexa_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return result


def __create_suggestions_table():
    db = __get_database()
    result = db.create_table(
        TableName='tvsuggestions',
        KeySchema=[
            {
                'AttributeName': 'alexa_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'id',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'alexa_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return result


# example on how to update
# def set_show_watch_status(alexaid, show_id, value):
#     table = __get_table()
#     response = table.update_item(
#         Key={
#             'alexa_id': alexaid,
#             'id': show_id
#         },
#         UpdateExpression="set watching = :w",
#         ExpressionAttributeValues={
#             ':w': value
#         },
#         ReturnValues="UPDATED_NEW"
#     )
#     return response
