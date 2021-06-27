import json
import os
import pymysql


def lambda_handler(event, context):
    
    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    body = json.loads(event['body'])
    print(body)
    eventid = int(body['eventid'])
    status = body['status']
    
    try:
        connection = pymysql.connect(host=endpoint,
                         user=username,
                         password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                event_upd = "update event set status = %s where eventid = %s;"
                cursor.execute(event_upd, (status, eventid))
            connection.commit()
            
        payload = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
            'body': 'Event updated successfully.'
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