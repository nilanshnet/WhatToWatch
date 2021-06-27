import json
import os
import pymysql


def lambda_handler(event, context):
    
    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    userid = event['queryStringParameters']['userid']
    print(event)
    
    try:
        connection = pymysql.connect(host=endpoint,
                         user=username,
                         password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        
        with connection:
            with connection.cursor() as cursor:
                watchnow_show = "select id, type, poster_path, min(episode) as episode, season from watchnow \
                                   join (select userid, id, min(season) as season from watchnow \
                                   where userid = %s \
                                   group by userid, id) as temp \
                                   using(userid, id, season) \
                                   group by id, type, poster_path, season;"
                cursor.execute(watchnow_show, (userid))
                watchnow = cursor.fetchall()
                # if watchnow[0]['id'] is None:
                #     watchnow = list()
   
            with connection.cursor() as cursor:
                watchlisttv_show = "select id, type, poster_path, release_date from watchlist where userid = %s and type = 'tv';"
                cursor.execute(watchlisttv_show, (userid))
                watchlisttv = cursor.fetchall()
  
            with connection.cursor() as cursor:
                watchlistmovie_show = "select id, type, poster_path, release_date from watchlist where userid = %s and type = 'movie';"
                cursor.execute(watchlistmovie_show, (userid))
                watchlistmovie = cursor.fetchall()
    
        body = {
                'watchnow': watchnow,
                'watchlisttv': watchlisttv,
                'watchlistmovie' : watchlistmovie
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