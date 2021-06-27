import json
import boto3

def lambda_handler(event, context):
    
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table("data")
    scan_kwargs = {
        'ProjectionExpression': "id, genres, poster_path, title, release_date, #ty",
        'ExpressionAttributeNames': {"#ty": "type"}
    }
    response = table.scan(**scan_kwargs)
    items = response.get('Items', [])
    
    for i in items:
        dat = i['id'] + "," + i['title'] + "," + '|'.join(i['genres']) + "," + i['release_date'] + "," + i['type'] + "," + i['poster_path'] 
        print(dat)