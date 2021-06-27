import json
import os
import boto3

def lambda_handler(event, context):
    
  
    sender = os.environ['domain_email']
    message = json.loads(event['Records'][0]['body'])
    creator = message['creator']
    invitee = message['invitee']
    description = message['description']
    url = message['url']
    time = message['time']
    subject = "Invitation for a watch party"
    charset = "UTF-8"
    
    body = ("You have been invited a watch party by {0} \n"
             "Details: \n"
             "Description: {1} \n"
             "Time: {2} \n"
             "Link: {3} \n"
            ).format(creator, description, time, url)
    
    client = boto3.client('ses')
    
    try:
        response = client.send_email(
            Destination = {
                'ToAddresses': invitee
            },
            Message = {
                'Body': {
                    'Text': {
                        'Charset': charset,
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source = sender
        )
    except Exception as e:
        print(str(e))
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
