import json
import os
import pymysql


def lambda_handler(event, context):
    
    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    body = json.loads(event['body'])
    userid = body['userid']
    friendid = body['friendid']
    
    try:
        connection = pymysql.connect(host=endpoint,
                         user=username,
                         password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                friend_del = "delete from friend where userid = %s and friendid = %s;"
                cursor.execute(friend_del, (userid, friendid))
            connection.commit()
                
            payload = {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                    },
                'body': 'Removed friend from friendlist successfully'
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
