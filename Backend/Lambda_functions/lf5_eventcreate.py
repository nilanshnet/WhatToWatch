import json
import os
import pymysql
import boto3

def lambda_handler(event, context):
    
    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    body = json.loads(event['body'])
    creator = body['creator']
    description = body['description']
    time = body['time']
    url = body['url']
    invitee_list = body['invitee']
    try:
        invitee_list = [x.strip() for x in invitee_list.split(',')]
    except:
        payload = {
                'statusCode': 400,            
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                    },
                    
                'body': 'Please enter comma seperated values in the invitee list.'
            }
        return payload
    
    
    try:
        connection = pymysql.connect(host=endpoint,
                         user=username,
                         password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        with connection:
            for invitee in invitee_list:
                with connection.cursor() as cursor:
                    event_ins = "insert into event values (NULL, %s, %s, %s, %s, %s, 'pending');"
                    cursor.execute(event_ins, (description, time, invitee, creator, url))
                connection.commit()
                
            with connection.cursor() as cursor:
                event_ins = "insert into event values (NULL, %s, %s, %s, %s, %s, 'accepted');"
                cursor.execute(event_ins, (description, time, creator, creator, url))
            connection.commit()
            
        sqs = boto3.client('sqs')
        queue_url = sqs.get_queue_url(QueueName='watchparty')['QueueUrl']
        message = {
            'creator' : creator,
            'invitee' : invitee_list,
            'description' : description,
            'time' : time,
            'url' : url
        }
        sqs.send_message(QueueUrl=queue_url, DelaySeconds=10,
                     MessageBody=json.dumps(message))
            
        payload = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
            'body': 'Event created successfully'
        }
        return payload
    except Exception as e:
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