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
                user_show = "select name from user where userid = %s;"
                cursor.execute(user_show, (friendid))
                friendname = cursor.fetchall()
                if friendname:
                    friendname = friendname[0]['name']
                else:
                    payload = {
                        'statusCode': 200,
                        'headers': {
                            'Access-Control-Allow-Headers': '*',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST'
                            },
                        'body': 'User doesnt exist.'
                        }
                    return payload
                
            with connection.cursor() as cursor:
                friend_show = "select friendid from friend where userid = %s;"
                cursor.execute(friend_show, (userid))
                friend_list = cursor.fetchall()
                for friend in friend_list:
                    if friend['friendid'] == friendid:
                        payload = {
                            'statusCode': 200,
                            'headers': {
                                'Access-Control-Allow-Headers': '*',
                                'Access-Control-Allow-Origin': '*',
                                'Access-Control-Allow-Methods': 'OPTIONS,POST'
                                },
                            'body': 'Friend already added.'
                            }
                        return payload
                
            with connection.cursor() as cursor:
                friend_ins = "insert into friend values (%s, %s, %s);"
                cursor.execute(friend_ins, (userid, friendid, friendname))
            connection.commit()
                
            payload = {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                    },
                'body': 'Friend added successfully.'
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