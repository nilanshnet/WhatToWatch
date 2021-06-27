
#### No layers for this lambda function

import json
import boto3
import os
import time

def lambda_handler(event, context):
    
    dataset_grp_arn = os.environ['dataset_grp_arn']
    tracking_id = os.environ['tracking_id']
    # userid = event['queryStringParameters']['userid']
    # session_id = event['queryStringParameters']['session_id']
    # item_id = event['queryStringParameters']['item_id']
    # rating = event['queryStringParameters']['rating']

    body = json.loads(event['body'])
    print(body)
    userid = body['userid']
    session_id = body['session_id']
    item_id = body['item_id']
    rating = str(body['rating'])
 
   
    timestamp = int(time.time())

    
    personalize = boto3.client('personalize')
    personalize_runtime = boto3.client('personalize-runtime')
    personalize_events = boto3.client(service_name='personalize-events')

 
    event = {
            "itemId": item_id,
            "rating" : rating
        }
    event_json = json.dumps(event)
        
    try:
        personalize_events.put_events(
                trackingId = tracking_id,
                userId= userid,
                sessionId = session_id,
                eventList = [{
                    'sentAt': timestamp,
                    'eventType': 'EVENT_TYPE',
                    'properties': event_json
                    }]
                )
    
        payload = {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                
                'body': "Model updated successfully"
            }
        
        return payload
    
    except Exception as e:
        print(e)
        payload = {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
            'body': str(e)
                }
        return payload