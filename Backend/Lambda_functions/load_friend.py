import json
import os
import pymysql


def lambda_handler(event, context):
    
    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    userid = event['queryStringParameters']['userid']
    
    try:
        connection = pymysql.connect(host=endpoint,
                         user=username,
                         password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                friend_show = "select friendid, friendname from friend where userid = %s;"
                cursor.execute(friend_show, (userid))
                friend_list = cursor.fetchall()
                
            body = {
                'friend_list': friend_list
            }
            payload = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            
            'body': json.dumps(body)
        }
        print(payload)
        return payload
    except Exception as e:
        print(e)
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
