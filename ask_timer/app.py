
import json
import requests
import os

LINE_MESSAGING_ENDPOINT = os.environ.get('LINE_MESSAGING_ENDPOINT')
LINE_ACCESS_TOKEN = os.environ.get('LINE_ACCESS_TOKEN')
LINE_USER_ID = os.environ.get('LINE_USER_ID')

data = {
    "to": LINE_USER_ID,
    "messages": [
        {
            "type": "text",
            "text": '今日は何時に就寝しますか？\n①計測開始時間\n②就寝時間\n\n例)\n22:00\n1:00'
        }
    ]
}

body = json.dumps(data)

def lambda_handler(event, context):
    res = requests.post(
        f'{LINE_MESSAGING_ENDPOINT}/push',
        data=body,
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
        }
    )
    print(res)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "success!",
        }),
    }
