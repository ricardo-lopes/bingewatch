from boto3 import resource
from boto3.dynamodb.conditions import Key,Attr


def __get_database():
    return resource('dynamodb', region_name='eu-west-1')


def __get_table():
    return __get_database().Table('tvshows')


def get_current_show(alexaid):
    table = __get_table()
    response = table.scan(
        FilterExpression = Key('alexa_id').eq(alexaid) & Attr('watching').eq(True)
    )
    if response['Items']:
        return response['Items'][0]
    else:
        return None


def set_show_watch_status(alexaid, id, value):
    table = __get_table()
    response = table.update_item(
        Key={
            'alexa_id': alexaid,
            'id': id
        },
        UpdateExpression="set watching = :w",
        ExpressionAttributeValues={
            ':w': value
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


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
        "title": "seinfeld",
        "season": 10,
        "watching": True,
        "lastseen": "2010-01-18T00:00:00Z"
    }
    dexter = {
        "alexa_id": "testid1",
        "id": 2,
        "title": "dexter",
        "season": 4,
        "watching": False,
        "lastseen": "2013-01-18T00:00:00Z"
    }
    wire = {
        "alexa_id": "testid1",
        "id": 3,
        "title": "the wire",
        "season": 1,
        "watching": False,
        "lastseen": None
    }
    table = __get_table()
    table.put_item(Item=seinfeld)
    table.put_item(Item=dexter)
    table.put_item(Item=wire)


