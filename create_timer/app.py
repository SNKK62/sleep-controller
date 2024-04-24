import json
import datetime
from zoneinfo import ZoneInfo
import boto3
import requests
import os

dynamodb = boto3.resource('dynamodb')
TIMES_TABLE_NAME = os.environ.get('TIMES_TABLE_NAME')
LINE_MESSAGING_ENDPOINT = os.environ.get('LINE_MESSAGING_ENDPOINT')
LINE_ACCESS_TOKEN = os.environ.get('LINE_ACCESS_TOKEN')
LINE_USER_ID = os.environ.get('LINE_USER_ID')

def lambda_handler(event, context):
    table = dynamodb.Table(TIMES_TABLE_NAME)
    print(event)

    body = json.loads(event.get('body'))
    message = body.get('events')[0].get('message')

    user_text = message.get('text')
    reply_token = body.get('events')[0].get('replyToken')
    reply_text = {"type": 'text', "text": "了解です！"}

    data = {
        "replyToken": reply_token,
        "messages": [reply_text]
    }

    requests.post(
        f'{LINE_MESSAGING_ENDPOINT}/reply',
        data=json.dumps(data),
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
        }
    )
    dt = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    dt_str = dt.strftime('%Y-%m-%d')
    start, end = user_text.split('\n')
    if int(start.split(':')[0]) < 12:
        dt_tomorrow = dt + datetime.timedelta(days=1)
        dt_tomorrow_str = dt_tomorrow.strftime('%Y-%m-%d')
        start_time = f'{dt_tomorrow_str} {start}'
    else:
        start_time = f'{dt_str} {start}'
    if int(end.split(':')[0]) < 12:
        dt_tomorrow = dt + datetime.timedelta(days=1)
        dt_tomorrow_str = dt_tomorrow.strftime('%Y-%m-%d')
        end_time = f'{dt_tomorrow_str} {end}'
    else:
        end_time = f'{dt_str} {end}'

    table.put_item(
        Item={
            'id': 'new',
            'start': start_time,
            'end': end_time,
        }

    )
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "success!",
        }),
    }
