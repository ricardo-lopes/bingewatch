from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr


def __get_database():
    return resource('dynamodb', region_name='eu-west-1')


def __get_table():
    return __get_database().Table('tvshows')


def get_current_show(alexaid):
    table = __get_table()
    response = table.scan(
        FilterExpression=Key('alexa_id').eq(alexaid) & Attr('watching').eq(True)
    )
    if response['Items']:
        return response['Items'][0]
    return None


def get_all_shows(alexaid):
    table = __get_table()
    response = table.scan(
        FilterExpression=Key('alexa_id').eq(alexaid)
    )
    if response['Items']:
        return response['Items']
    return None


def set_show_watch_status(alexaid, show_id, value):
    table = __get_table()
    response = table.update_item(
        Key={
            'alexa_id': alexaid,
            'id': show_id
        },
        UpdateExpression="set watching = :w",
        ExpressionAttributeValues={
            ':w': value
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def clear_table(alexaid):
    table = __get_table()
    shows = get_all_shows(alexaid)
    with table.batch_writer() as batch:
        for s in shows:
            batch.delete_item(
                Key={
                    'alexa_id': s['alexa_id'],
                    'id': s['id']
                }
            )


def insert_show(alexaid, id, show_name):
    table = __get_table()
    show = {
        "alexa_id": alexaid,
        "id": id,
        "title": show_name
    }
    return table.put_item(Item=show)


def __create_table():
    db = __get_database()
    result = db.create_table(
        TableName='tvshows',
        KeySchema=[
            {
                'AttributeName':'alexa_id',
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


def __insert_data():
    seinfeld = {
        "alexa_id": "testid1",
        "id": 1,
        "title": "seinfeld"
    }
    dexter = {
        "alexa_id": "testid1",
        "id": 2,
        "title": "dexter"
    }
    wire = {
        "alexa_id": "testid1",
        "id": 3,
        "title": "the wire"
    }
    table = __get_table()
    table.put_item(Item=seinfeld)
    table.put_item(Item=dexter)
    table.put_item(Item=wire)


