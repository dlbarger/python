#   Script:     main.py
#   Function:   cdp-custprofile-api-<lane>
#   Handler:    main.lambda_handler
#   Author:     Dennis Barger, SEI

import json
import boto3
from boto3.dynamodb.conditions import Key
import pprint

client = boto3.resource('dynamodb')
tablename = 'cdp-customerprofile'

def lambda_handler(event, context):
    
    
    custkey = event['queryStringParameters']['customerkey']
    tbl = client.Table(tablename)
    response = tbl.query(
        KeyConditionExpression=Key('customerKey').eq(custkey)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }

def query_cust_profile(customerKey, table, dyno_client):

    response = dyno_client.query(
        TableName = table,
        KeyConditionExpression = 'customerKey = :key',
        ExpressionAttributeValues = {
            ':key': { 'S': customerKey}
        }
    )

