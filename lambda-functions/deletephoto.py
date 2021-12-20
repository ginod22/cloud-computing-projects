import json
import boto3 
from boto3.dynamodb.conditions import Key, Attr

REGION="us-east-1"
dynamodb = boto3.resource('dynamodb',region_name=REGION)
table = dynamodb.Table('PhotoGallery')

                            
def lambda_handler(event, context):
	photoID=event['params']['path']['id']
	
	tableItems = table.scan(
	    FilterExpression=Key('PhotoID').eq(photoID)
	)
	
	items = tableItems['Items']
	creationTime = items[0]['CreationTime']

    
	table.delete_item(
		Key={
			'PhotoID': photoID,
			'CreationTime': int(creationTime),
		}
	)

	return {
        "statusCode": 200,
        "body": json.dumps(photoID)
    }