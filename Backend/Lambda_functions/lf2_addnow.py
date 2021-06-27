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
    userid = body['userid']
    name = body['name']
    poster_path = body['poster_path']
    type = body['type']
    id = body['id']
    
    try:
        connection = pymysql.connect(host=endpoint,
                         user=username,
                         password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
                         
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.Table("data")
        response = table.get_item(Key = {"id": id})    

        with connection:
            if type == 'tv':
                season_num = 0
                for season in response['Item']['seasons']:
                    season_num += 1
                    episode = 0
                    for _ in season['episodes']:
                        episode += 1
                        with connection.cursor() as cursor:
                            watchnow_ins = "insert into watchnow values (%s, %s, %s, %s, %s, %s, %s);"
                            cursor.execute(watchnow_ins, (userid, name, id, type, poster_path, episode, season_num))
                        connection.commit()
                        
            elif type == 'movie':
                with connection.cursor() as cursor:
                    watchnow_ins = "insert into watchnow values (%s, %s, %s, %s, %s, 'NA', 'NA');"
                    cursor.execute(watchnow_ins, (userid, name, id, type, poster_path))
                connection.commit()

            
            with connection.cursor() as cursor:
                watchlist_del = "delete from watchlist where userid = %s and id = %s;"
                cursor.execute(watchlist_del, (userid, id))
            connection.commit()
            
                
        payload = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
            'body': 'Added to watchnow successfully'
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
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                    'body': str(e)
                }
        return payload