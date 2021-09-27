import os
import boto3
import requests
import uuid

ssm = boto3.client(
    'ssm',
    region_name="us-east-1",
    aws_access_key_id=os.environ['ACCESS_KEY'],
    aws_secret_access_key=os.environ['SECRET_KEY']
)

ssm_response = ssm.get_parameter(
    Name='FlaskAPIKey',
    WithDecryption=True
)

subscription_key = ssm_response['Parameter']['Value']
endpoint = "https://westus.api.cognitive.microsoft.com"


def get_sentiment(input_text, input_language):
    path = '/text/analytics/v3.0/sentiment'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = {
        'documents': [
            {
                'language': input_language,
                'id': '1',
                'text': input_text
            },
        ]
    }
    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()
