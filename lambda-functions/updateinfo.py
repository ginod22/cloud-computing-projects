import json
import boto3  
import time
from boto3.dynamodb.conditions import Key, Attr

REGION="us-east-1"
dynamodb = boto3.resource('dynamodb',region_name=REGION)
table = dynamodb.Table('PhotoGallery')

def lambda_handler(event, context):
    
    photoID=event['params']['path']['id']
    title=event['body-json']['title']
    description=event['body-json']['description']
    tags=event['body-json']['tags']
    
    tableItems = table.scan(
        FilterExpression=Key('PhotoID').eq(photoID)
    )
    items = tableItems['Items']
    creationTime = items[0]['CreationTime']
    
    
    response = table.update_item(
        Key={
            'PhotoID': photoID,
            'CreationTime': int(creationTime),
        },
        UpdateExpression="set Description =:d, Tags=:ta, Title=:ti",
        ExpressionAttributeValues={
            ':d': description,
            ':ta': tags,
            ':ti': title,
        },
        ReturnValues= 'UPDATED_NEW'
    )
    
    return response