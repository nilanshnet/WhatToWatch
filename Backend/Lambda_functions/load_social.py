import json
import os
import pymysql


def lambda_handler(event, context):
    
    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    userid = event['queryStringParameters']['userid']
    invitee = event['queryStringParameters']['useremail']
    friend_list = list()
    friend_watchlist = list()
    
    try:
        connection = pymysql.connect(host=endpoint,
                         user=username,
                         password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                friend_show = "select friendid from friend where userid = %s;"
                cursor.execute(friend_show, (userid))
                friend_list = cursor.fetchall()

            for friend in friend_list:
                with connection.cursor() as cursor:
                    watchnow_show = "select name, poster_path from watchnow group by name, poster_path, userid having userid = %s limit 3;"
                    cursor.execute(watchnow_show, (friend['friendid']))
                    rows = cursor.fetchall()
                    watchnow_list = list()
                    if rows:
                        temp_name = rows[0]['name']
                        watchnow_dict = dict()
                        for row in rows:
                            watchnow_dict = {'name': temp_name, 'poster_path': row['poster_path']}
                            watchnow_list.append(watchnow_dict)
                    friend_watchlist += watchnow_list
                    
            with connection.cursor() as cursor:
                event_show = "select eventid, description, time, creator, url from event where invitee = %s and status = 'pending';"
                cursor.execute(event_show, (invitee))
                pending_events = cursor.fetchall()
            
            with connection.cursor() as cursor:
                event_show = "select eventid, description, time, creator, url from event where invitee = %s and status = 'accepted';"
                cursor.execute(event_show, (invitee))
                confirmed_events = cursor.fetchall()

        body = {
                'friend_watchlist': friend_watchlist,
                'pending_events' : pending_events,
                'confirmed_events' : confirmed_events
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