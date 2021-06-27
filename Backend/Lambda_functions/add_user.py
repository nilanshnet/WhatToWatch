import json
import os
import pymysql


def lambda_handler(event, context):
    
    print(event)
    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    attributes = event['request']['userAttributes']
    userid = event['userName']
    name = attributes['name']
    email = attributes['email']
    
    try:
        connection = pymysql.connect(host=endpoint,
                         user=username,
                         password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                user_ins = "insert into user(userid, name, email) values (%s, %s, %s);"
                cursor.execute(user_ins, (userid, name, email))
            connection.commit()
                
            
        return event  
    except Exception as e:
        print(e)

            
        return event 
