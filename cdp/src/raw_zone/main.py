"""
Function:   cdp-custprofile-rzconsumer
Script:     main.py
Handler:    main.lambda_handler
Author:     Dennis Barger, SEI

"""

import json
import boto3
import io
from cloudevents.http import CloudEvent, to_structured
import time

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Get Guest Cards temporarily saved in S3
        data = get_s3_object(
            bucket = event['Staging']['bucket'],
            key = event['QueryResults'],
            client=s3
        )

        # Build cloudevent message
        attributes = {
            "type": "AvalonBay.Sfdc.DatabaseEventHandler.Models.AddEventModel.v1",
            "source": "PropMgmt/EventStream",
            "subject": "Prospect/Update"
        }
        message = CloudEvent(attributes, json.loads(data))
        headers, body = to_structured(message)

        # Set S3 object key
        ts = time.time()
        key = event['Destination']['folder'] + '/PropMgmt' + '-'+ str(ts)

        # Write Guest Cards in cloudevent format to target S3 bucket
        response = put_s3_object(
            object = body.decode('utf-8'), 
            bucket = event['Destination']['bucket'], 
            key = key,
            client=s3
        )

        return(response)

    except Exception as e:
        raise(e)

def get_s3_object(bucket, key, client):
    try:
        obj = client.get_object(
            Bucket = bucket,
            Key = key
        )
        response = obj['Body'].read().decode('utf-8')
        return(response)
    except Exception as e:
        raise(e)

def put_s3_object(object, bucket, key, client):
    try:
        response = client.put_object(
            Bucket = bucket,
            Key = key,
            Body = object
        )
        return(response)
    except Exception as e:
        raise(e)