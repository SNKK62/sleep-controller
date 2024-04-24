
import json
import requests
import os
import boto3
from boto3.dynamodb.conditions import Key
import datetime
from zoneinfo import ZoneInfo

dynamodb = boto3.resource('dynamodb')
TIMES_TABLE_NAME = os.environ.get('TIMES_TABLE_NAME')
LINE_MESSAGING_ENDPOINT = os.environ.get('LINE_MESSAGING_ENDPOINT')
LINE_ACCESS_TOKEN = os.environ.get('LINE_ACCESS_TOKEN')
LINE_USER_ID = os.environ.get('LINE_USER_ID')

data = {
    "to": LINE_USER_ID,
    "messages": [
        {
            "type": "text",
            "text": '就寝を確認しました．'
        }
    ]
}

body = json.dumps(data)

def lambda_handler(event, context):
    table = dynamodb.Table(TIMES_TABLE_NAME)
    res = table.query(
        KeyConditionExpression=Key("id").eq("new")
    )

    items = res.get('Items')

    if len(items) > 0:
        start_str = items[0].get('start')
        now_str = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).strftime('%Y-%m-%d %H:%M')
        start = datetime.datetime.strptime(start_str, '%Y-%m-%d %H:%M')
        now = datetime.datetime.strptime(now_str, '%Y-%m-%d %H:%M')
        if now > start:
            table.delete_item(
                Key={
                    'id': 'new'
                }
            )
            requests.post(
                f'{LINE_MESSAGING_ENDPOINT}/push',
                data=body,
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
                }
            )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "success!",
        }),
    }
