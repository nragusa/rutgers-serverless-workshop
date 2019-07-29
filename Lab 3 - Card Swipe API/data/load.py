#!/usr/bin/python

import boto3
import csv
from botocore.exceptions import ClientError

TARGET_TABLE = 'rutgers-card-swipe-dev'
TARGET_REGION = 'us-east-2'
NAME_FILE = 'names.csv'

# Load CSV file into list
source = []
with open(NAME_FILE) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        source.append(row)

# Batch write items into DynamoDB
target_ddb = boto3.resource('dynamodb', region_name=TARGET_REGION)
table = target_ddb.Table(TARGET_TABLE)
with table.batch_writer() as batch:
    for i in range(len(source)):
        try:
            batch.put_item(
                Item={
                    'student_id': source[i][0],
                    'first_name': source[i][1],
                    'last_name': source[i][2]
                })
        except ClientError as e:
            print('Problem loading item into Dynamo: {}'.format(e))