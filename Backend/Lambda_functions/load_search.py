import json
import boto3
import os
import pymysql
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection

def lambda_handler(event, context):
    
    endpoint = os.environ['endpoint']
    username = os.environ['user']
    password = os.environ['password']
    db = os.environ['database']
    es_host = os.environ['es_host']
    region = os.environ['region']
    campaign_arn = os.environ['campaign_arn']
    service = "es"
    userid = event['queryStringParameters']['userid']
    
    
    try:
        connection = pymysql.connect(host=endpoint,
                         user=username,
                         password=password,
                         database=db,cursorclass=pymysql.cursors.DictCursor)
        
        with connection:
            with connection.cursor() as cursor:
                trending_show = "select id, type, poster_path, release_date from trending"
                cursor.execute(trending_show)
                trending = cursor.fetchall()
            
            with connection.cursor() as cursor:
                preference_show = "select genre from preference where userid = %s"
                cursor.execute(preference_show, (userid))
                genre_list = cursor.fetchall()
        
        credentials = boto3.Session().get_credentials()
        auth = AWSRequestsAuth(aws_access_key=credentials.access_key,
                           aws_secret_access_key=credentials.secret_key,
                           aws_host=es_host,
                           aws_region=region,
                           aws_service=service,
                           aws_token=credentials.token)
    
        es_client = Elasticsearch(
            host = es_host,
            port = 443,
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
        
        preference = list()
        for search_key in genre_list:
            query = {
                "size" : 14 // len(genre_list),
                "sort": [
                        { "_score" : "desc" }
                    ],
                "query": {
                    "match": {
                        "genere": search_key['genre'],
                    }
                }
            }
            response = es_client.search(body=query, index='search_genre')
            for hit in response['hits']['hits']:
                del hit['_source']['genere']
                del hit['_source']['title']
                preference.append(hit['_source'])
        
        recommendation = list()
        recommend_client = boto3.client('personalize-runtime')
        response = recommend_client.get_recommendations(
                        campaignArn=campaign_arn,
                        userId=userid,
                        numResults=14)
                        
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.Table("data")
        
        for item in response['itemList']:
            db_response = table.get_item(
                            Key = {"id": item['itemId']}, 
                            ProjectionExpression = "id, #ty, poster_path, release_date",
                            ExpressionAttributeNames={'#ty': 'type'})
            recommendation.append(db_response['Item'])
        
        
        body = {
                'trending': trending,
                'preference' : preference,
                'recommendation' : recommendation
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