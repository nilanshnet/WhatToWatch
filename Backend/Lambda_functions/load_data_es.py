### used for storing data into elastic search
# below are the layers for the Lambda function
""" 
    Name                                layer version   Version ARN
1	Klayers-python38-aws-requests-auth	8	            arn:aws:lambda:us-east-1:770693421928:layer:Klayers-python38-aws-requests-auth:8
2	Klayers-python38-elasticsearch	    22	            arn:aws:lambda:us-east-1:770693421928:layer:Klayers-python38-elasticsearch:22
3	Klayers-python38-requests	        16	            arn:aws:lambda:us-east-1:770693421928:layer:Klayers-python38-requests:16
 """
import json
import os
import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection

def lambda_handler(event, context):
    
    es_host = os.environ['es_host']
    region = os.environ['region']
    service = "es"
    
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
    
    # dynamodb = boto3.resource("dynamodb", region_name=region)
    # table = dynamodb.Table("data")
    # response = table.get_item(Key = {"id": 'mv_10144'}) 
    es_client.delete_by_query(index="search_genre", body={"query": {"match_all": {}}})
    
    # title = "Little Mermaid"
    # genre = ['action', 'fantasy']
    # id = 'mv_10144'
    # type = 'movie'
    # poster_path = 'https://image.tmdb.org/t/p/w500/9nJ9rm6RwYgIggnGVy8Dej4olef.jpg'
    
    # body = {'title':title,'genre':genre, 'id':id, 'type':type, 'poster_path':poster_path}
    
    # res = es_client.index(index="search_genre",body=json.dumps(body))
    # print(res)