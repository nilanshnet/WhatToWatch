import json
import os
import pymysql


def lambda_handler(event, context):
    print(event)

    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    body = json.loads(event['body'])
    userid = body['userid']
    genres = body['genre']
    
    try:
        connection = pymysql.connect(host=endpoint,
                             user=username,
                             password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:  
                preference_del = "delete from preference where userid = %s;"
                cursor.execute(preference_del, (userid))
            connection.commit()
            
            with connection.cursor() as cursor:
                preference_ins = "insert into preference (userid, genre) values (%s, %s);"
                for genre in genres:
                    cursor.execute(preference_ins, (userid, genre))
            connection.commit()
                    
        payload = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
            'body': 'Edit successful'
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
        