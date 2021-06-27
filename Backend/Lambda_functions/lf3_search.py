#layers for the lambda function

"""
Merge order     Name                                Layer version                Version ARN
1	            Klayers-python38-elasticsearch	    22	                arn:aws:lambda:us-east-1:770693421928:layer:Klayers-python38-elasticsearch:22
2	            Klayers-python38-requests	        16	                arn:aws:lambda:us-east-1:770693421928:layer:Klayers-python38-requests:16
3	            Klayers-python38-aws-requests-auth	8	                arn:aws:lambda:us-east-1:770693421928:layer:Klayers-python38-aws-requests-auth:8
"""

# python code 
import json
import boto3
import os
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection

def lambda_handler(event, context):
    
    search_key = event['queryStringParameters']['q']
    region = os.environ['region']
    es_host = os.environ['es_host']
    service = "es"
    
    try:
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
        
        query = {
                "sort": [
                        { "_score" : "desc" }
                    ],
                "query": {
                    "match": {
                        "title": search_key,
                    }
                }
            }
        
        response = es_client.search(body=query, index='search_genre')
        results = list()
        for hit in response['hits']['hits']:
            results.append(hit['_source'])
        
        query = {
                "sort": [
                        { "_score" : "desc" }
                    ],
                "query": {
                    "match": {
                        "genere": search_key,
                    }
                }
            }
        
        response = es_client.search(body=query, index='search_genre')

        for hit in response['hits']['hits']:
            results.append(hit['_source'])
        
        payload = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps(results),
        }
        return payload
        
    except Exception as e:
        payload = {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Headers': '*',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,GET'
                         },
                    'body': str(e),
                }
        return payload
