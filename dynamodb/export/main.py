'''
Script:     main.py
Author:     Dennis Barger, SEI
Date:       2/11/22

Description:
Export all items from DynamoDB table using Boto3 and upload
to S3 bucket.

'''
import json
import boto3 
import csv

dynamodb = boto3.resource('dynamodb')

def get_data(tableName):

    table = dynamodb.Table(tableName)
    response = table.scan()

    return(response['Items'])

def lambda_handler(event, context):
    results = get_data(event['tableName'])
    return(results)

if __name__ == "__main__":

    context = {}
    event = {
        "tableName": "leasable-engine-service-categories-table-dev"
    }

    data = lambda_handler(event, context)
    json_data = json.dumps(data, indent=4)
    print(json_data)

    
