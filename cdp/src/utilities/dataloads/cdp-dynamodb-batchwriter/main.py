"""
Function:   avb-dev-cdp-batchwriter
Script:     main.py
Handler:    main.lambda_handler

Description:
Load S3 data in batches to DynamoDB table.

Event Parameter:

{
    "bucket": "cdp-customerhub",
    "key": "",
    "table": "cdp-customerprofile",
    "entity": ""
}
"""

import json
import boto3
import os 
import csv 
import codecs
import sys

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

def set_customer(batch):
    response = {
        'customerKey':          str(batch['customerKey']).strip(),
        'customerSortKey':      str(batch['customerSortKey']).strip(),
        'firstName':            str(batch['firstName']).strip(),
        'lastName':             str(batch['lastName']).strip(),
        'email':                str(batch['email']).strip(),
        'gender':               str(batch['gender']).strip(),
        'birthdate':            str(batch['birthdate']).strip()
    }
    return(response)

def set_lease(batch):
    response = {
        'customerKey':          str(batch['customerKey']).strip(),
        'customerSortKey':      str(batch['customerSortKey']).strip(),
        'address':              str(batch['address']).strip(),
        'city':                 str(batch['city']).strip(),
        'zipCode':              str(batch['zipCode']).strip(),
        'customerType':         str(batch['customerType']).strip(),
        'moveInDate':           str(batch['moveInDate']).strip(),
        'moveOutDate':          str(batch['moveOutDate']).strip()
    }
    return(response)

def set_browsehist(batch):
    response = {
        'customerKey':          str(batch['customerKey']).strip(),
        'customerSortKey':      str(batch['customerSortKey']).strip(),
        'ipAddress':            str(batch['ip_address']).strip(),
        'activityTimestamp':    str(batch['activity_timestamp']).strip(),
        'activityDate':         str(batch['activity_date']).strip(),
        'appName':              str(batch['app_name']).strip(),
        'url':                  str(batch['url']).strip(),
        'topLevelDomain':       str(batch['top_level_domain']).strip(),
        'userAgent':            str(batch['user_agent']).strip()
    }
    return(response)


def lambda_handler(event, context):
    try:
        BUCKET = event['bucket']
        KEY = event['key']
        TABLENAME = event['table']
        ENTITY = event['entity']

        obj = s3.Object(BUCKET, KEY).get()['Body']
        dyno_table = dynamodb.Table(TABLENAME)
        batch_size = 100
        batch = []

        for row in csv.DictReader(codecs.getreader('utf-8')(obj)):
            if ENTITY == 'customer':
                item = set_customer(row)

            if ENTITY == 'lease':
                item = set_lease(row)

            if ENTITY == 'browsehist':
                item = set_browsehist(row)

            if len(batch) >= batch_size:
                write_to_dynamo(batch, dyno_table)
                batch.clear()
            batch.append(item)
        if batch:
            write_to_dynamo(batch, dyno_table)

        return {
            'statusCode': 200,
            'body': json.dumps('Success')
        }
    except Exception as e:
        raise(e)

def write_to_dynamo(rows, table):
    try:
        with table.batch_writer() as batch:
            for i in range(len(rows)):
                batch.put_item(Item=rows[i])

    except Exception as e:
        raise(e)