import json
import boto3
import decimal
from elasticsearch import Elasticsearch


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def get_data_kibana(search_key):
    try:
        kibana_url = "https://search-search-3mcuwao2dej7a5mg4w75pnfj7m.us-east-1.es.amazonaws.com/"
        es = Elasticsearch(
            [kibana_url],
            http_auth=("naga", "Nagasai@123"),
        )
        query_body = {
            "size": 15,
            "from": 0,
            "query": {
                "match": {
                    "genere": str(search_key),
                }
            }
        }
        result_genre = es.search(index="search_genre", body=query_body)
        result_genre = parse_kibana_response(result_genre['hits']['hits'])
        query_body = {
            "size": 15,
            "from": 0,
            "query": {
                "match": {
                    "title": str(search_key),
                }
            }
        }
        result_title = es.search(index="search_genre", body=query_body)
        result_title = parse_kibana_response(result_title['hits']['hits'])
        return result_title + result_genre
    except Exception as ex:
        print(ex)
        return []


def parse_kibana_response(temp_1):
    temp_list = []
    for items in temp_1:
        temp_list.append([items['_score'], items['_source']['id']])
    sorted(temp_list, key=lambda x: x[0])
    return temp_list


def get_details_single(mv_id):
    session = boto3.Session(
        aws_access_key_id='AKIAV4XBFVS6MPVLBKES',
        aws_secret_access_key='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',
    )
    db_resource = session.resource('dynamodb', region_name='us-east-1')
    db_table = db_resource.Table('data')
    response = db_table.get_item(
        Key={
            'id': mv_id
        })
    get_item = response.get('Item', None)
    return get_item


def get_details_batch(list_id):
    session = boto3.Session(
        aws_access_key_id='AKIAV4XBFVS6MPVLBKES',
        aws_secret_access_key='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',
    )
    db_resource = session.resource('dynamodb', region_name='us-east-1')
    # db_table = db_resource.Table('data')
    temp_list = []
    for items in list_id:
        temp_list.append({'id': items[1]})

    try:
        response_db = db_resource.batch_get_item(
            RequestItems={
                'data': {
                    'Keys': temp_list,
                    'ConsistentRead': True
                }
            },
            ReturnConsumedCapacity='TOTAL'
        )
    except Exception as ex:
        print(ex)
    else:
        return json.dumps(response_db['Responses']['data'], cls=DecimalEncoder)
        

def lambda_handler(event, context):
    print(event)
    print(context)
    search_key = event['queryStringParameters']['q']
    try:
        response_es = get_data_kibana(search_key)
        movies_list = get_details_batch(response_es)
        print(movies_list)
    except Exception as ex:
        print(ex)
        movies_list = []
    
    return {

        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': movies_list
    }
