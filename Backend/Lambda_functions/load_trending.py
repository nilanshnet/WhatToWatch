
# This file is as the trending_list.csv file inside the lambda along with function.py file

""" 
mv_299534,movie,https://image.tmdb.org/t/p/w500/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg
mv_12445,movie,https://image.tmdb.org/t/p/w500/da22ZBmrDOXOCDRvr8Gic8ldhv4.jpg
tv_1399,tv,https://image.tmdb.org/t/p/w500/u3bZgnGQ9T01sWNhyveQz0wH0Hl.jpg
tv_1668,tv,https://image.tmdb.org/t/p/w500/f496cm9enuEsZkSPzCwnTESEK5s.jpg
tv_66732,tv,https://image.tmdb.org/t/p/w500/x2LSRK2Cm7MZhjluni1msVJ3wDF.jpg
mv_1865,movie,https://image.tmdb.org/t/p/w500/8fxendLObfOewRllxiM4X9Ey7S4.jpg
 """

import json
import os
import pymysql

def lambda_handler(event, context):
    
    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    
    try:
        connection = pymysql.connect(host=endpoint,
                         user=username,
                         password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        
        with connection:
            with open("trending_list.csv", encoding = 'utf-8') as f:
                for line in f:
                    id, type, poster_path = line.split(",")
                    with connection.cursor() as cursor:
                        trending_ins = "insert into trending (id, type, poster_path) values (%s, %s, %s)"
                        cursor.execute(trending_ins, (id, type, poster_path))
                    connection.commit()
    
        print("Trending loaded successfully")
            
    except Exception as e:
        print(e)
        
