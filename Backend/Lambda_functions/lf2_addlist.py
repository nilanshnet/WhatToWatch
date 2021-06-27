import json
import os
import pymysql


def lambda_handler(event, context):
    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    
    body = json.loads(event['body'])
    print(event)
    print(body)
    userid = body['userid']
    poster_path = body['poster_path']
    type = body['type']
    id = body['id']
    release_date = body['release_date']
    
    try:
        connection = pymysql.connect(host=endpoint,
                         user=username,
                         password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                watchlist_show = "select * from watchlist where userid = %s and id = %s;"
                cursor.execute(watchlist_show, (userid, id))
                if cursor.fetchall():
                    payload = {
                        'statusCode': 200,
                        'headers': {
                            'Access-Control-Allow-Headers': '*',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST'
                        },
                        'body': 'Watchlist'
                    }
                    return payload
                        
            with connection.cursor() as cursor:            
                watchnow_show = "select * from watchnow where userid = %s and id = %s;"
                cursor.execute(watchnow_show, (userid, id))
                if cursor.fetchall():
                    payload = {
                        'statusCode': 200,
                        'headers': {
                            'Access-Control-Allow-Headers': '*',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST'
                        },
                        'body': 'WatchNow'
                    }
                    return payload
                        
            with connection.cursor() as cursor:
                watchlist_ins = "insert into watchlist (userid, id, type, poster_path, release_date) values (%s, %s, %s, %s, %s);"
                cursor.execute(watchlist_ins, (userid, id, type, poster_path, release_date))
            connection.commit()
            
                
        payload = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body':  'Success'
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