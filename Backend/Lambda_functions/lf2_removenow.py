import json
import os
import pymysql


def lambda_handler(event, context):
    
    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    userid = event['userid']
    id = event['id']
    
    try:
        connection = pymysql.connect(host=endpoint,
                         user=username,
                         password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                watchnow_del = "delete from watchnow where userid = %s and id = %s;"
                cursor.execute(watchnow_del, (userid, id))
            connection.commit()
            
            with connection.cursor() as cursor:
                watchnowhistory_upd = "update watchhistory set status = 'stopped' where userid = %s and id = %s;"
                cursor.execute(watchnowhistory_upd, (userid, id))
            connection.commit()
                
            payload = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': 'Stopped watching Movie/show'
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
