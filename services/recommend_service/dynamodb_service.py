import boto3
import dotenvals 
from decimal import Decimal
from services.recommend_service.models.trained_q_table import Q_TABLE
import dotenvals


region = dotenvals.REGION_NAME
AWS_ACCESS_KEY_ID = dotenvals.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = dotenvals.AWS_SECRET_ACCESS_KEY


def get_dynamodb():

    return boto3.resource('dynamodb',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY,region_name=region)   


def create_Dynamo_table(table_name):
    dynamodb = get_dynamodb()
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'state',
                'KeyType': 'HASH'
            } , 
            {
                'AttributeName': 'action',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'state',
                'AttributeType': 'N'
            } ,
            {
                'AttributeName': 'action',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    return table


def init_dynamo_table(table_name):
    dynamodb = get_dynamodb()
    table = dynamodb.Table(table_name)
    
    values = Q_TABLE
    
    for action, state, q in values:
        table.put_item(
            Item={
                'state': state,
                'action': action,
                'q': q
            }
        )

    print (' Q Table initialized with pre trained model')

    return table

def init_dynamo_table_with_zero(table_name ,states , actions):
    dynamodb = get_dynamodb()
    table = dynamodb.Table(table_name)
    
    with table.batch_writer() as batch:
        for state in states:
            for action in actions:
                batch.put_item(
                    Item={
                        'state': state,
                        'action': action,
                        'q': 0
                    }
                )
    
    print (' Q Table initialized with zeros')
    

    return table


def get_q_from_dynamo(table_name, state, action):
    dynamodb = get_dynamodb()
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'state': int(state),
            'action': int(action)
        }
    )
    item = response.get('Item')
    if item:
        return item['q']
    else:
        return None


def get_action_with_max_q(table_name, state):
    dynamodb = get_dynamodb()
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression='#s = :state',
        ExpressionAttributeNames={'#s': 'state'},
        ExpressionAttributeValues={':state': int(state)}  # Convert state to int if it's a Number
    )
    items = response['Items']
    max_q = Decimal('0')
    action = 0
    for item in items:
        item_q = item['q']
        if item_q > max_q:
            max_q = item_q
            action = item['action']
    return action


def update_q_value_in_q_table(table_name, state, action, new_q):
    dynamodb = get_dynamodb()
    table = dynamodb.Table(table_name)
    
    response = table.update_item(
        Key={
            'state': int(state),
            'action': int(action)
        },
        UpdateExpression='SET q = :val',
        ExpressionAttributeValues={
            ':val': new_q
        },
        ReturnValues='UPDATED_NEW'
    )

    
    return response
