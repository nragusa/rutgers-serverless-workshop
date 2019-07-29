import boto3
import json
import os

from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

# Constants
DDB_TABLE = os.environ['DDB_TABLE']
DDB = boto3.resource('dynamodb')
TABLE = DDB.Table(DDB_TABLE)


def get_student(event, context):
    """Returns a student ID, first, and last name given a Student ID."""
    return_code = 200
    try:
        if event['queryStringParameters'] is not None:
            student_id = event['queryStringParameters']['student_id']
            response = TABLE.query(
                KeyConditionExpression=Key('student_id').eq(student_id))
            # A valid student with this ID was found
            if len(response['Items']) == 1:
                body = {
                    'student_id': student_id,
                    'first_name': response['Items'][0]['first_name'],
                    'last_name': response['Items'][0]['last_name']
                }
            else:
                body = {'error': 'Student ID not found'}
                return_code = 404
        else:
            # student_id was not passed as a query parameter
            body = {
                'error':
                'Invalid query, must pass student_id as query string parameter'
            }
            return_code = 400
    except KeyError:
        # An invalid query string was passed
        body = {'error': 'Invalid student_id passed'}
        return_code = 400
    except ClientError as e:
        # Problem getting an item from DynamoDB
        body = {'error': 'Problem querying DynamoDB: {}'.format(e)}
        return_code = 500
    response = {'statusCode': return_code, 'body': json.dumps(body)}
    return response


def add_student(event, context):
    """Adds a student ID, first and last name to a DynamoDB table."""
    return_code = 200
    try:
        body = json.loads(event['body'])
        student_id = body['student_id']
        first_name = body['first_name']
        last_name = body['last_name']
        response = TABLE.put_item(
            Item={
                'student_id': student_id,
                'first_name': first_name,
                'last_name': last_name
            })
        body = {'status': 'OK'}
    except json.decoder.JSONDecodeError as e:
        # The request contained invalid JSON
        body = {'error': 'Invalid JSON: {}'.format(e)}
        return_code = 400
    except KeyError as e:
        # Valid JSON passed but was missing one of the required inputs
        body = {'error': 'Missing information in request: {}'.format(e)}
        return_code = 400
    except ClientError as e:
        # Problem adding / updating the item in DynamoDB
        body = {'error': 'Problem inserting item into DynamoDB: {}'.format(e)}
        return_code = 500
    return {'statusCode': return_code, 'body': json.dumps(body)}
