import json


def hello(event, context):
    body = {"message": "Hello Rutgers!"}

    response = {"statusCode": 200, "body": json.dumps(body)}

    try:
        print('Agent: {}'.format(event['headers']['User-Agent']))
        print('IP: {}'.format(event['headers']['X-Forwarded-For']))
    except KeyError:
        print('No headers to print')

    return response
