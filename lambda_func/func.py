import json
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyTable')
def lambda_handler(event, context):
    response = table.get_item(Key={
        'id':'0'
    })
    views = response['Item']['Views']
    views = views + 1
    print(views)
    response = table.put_item(Item={
            'id':'0',
            'Views': views
    })

    return views