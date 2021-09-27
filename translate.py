import boto3
import os
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
location = 'westus'


def get_translation(text_input, language_output):
    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=' + language_output
    constructed_url = base_url + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text_input
    }]
    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()
