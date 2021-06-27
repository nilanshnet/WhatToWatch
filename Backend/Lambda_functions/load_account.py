import json
import os
import pymysql


def lambda_handler(event, context):
    print(event)
    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    userid = event['queryStringParameters']['userid']
    genre = list()
    
    try:
        connection = pymysql.connect(host=endpoint,
                             user=username,
                             password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:  
                cursor = connection.cursor()
                preference_show = "select * from preference where userid = %s;"
                cursor.execute(preference_show, (userid))
                for row in cursor.fetchall():
                    genre.append(row['genre'])
        
        payload = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps(genre)
       
        }
        return payload
        
    except Exception as e:
        payload = {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
                },
            'body': str(e)
                }
        return payload
        