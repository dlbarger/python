"""
Author: Dennis Barger
Date:   2/19/22

Lambda function to read and parse receipt image.  The function
leverages the AWS textract services via boto2.  Specifically
the function uses the Analyze Expense API within the textract
service.

Parameters

event:
{
    "s3": {
        "source": {
            "bucket": "string",
            "key": "string"
        },
        "target": {
            "bucket": "string",
            "key": "string"
        }
    }
}
"""

import boto3
import json

textract = boto3.client('textract', region_name = 'us-east-1')
s3 = boto3.resource('s3')

def put_object(bucket, key, data):
    obj = s3.Object(bucket, key)

    response = obj.put(
        Body = (bytes(json.dumps(data).encode('UTF-8')))
    )

    return(response)


def parse_receipt(content):
    response = textract.analyze_expense(
        Document = {
            'S3Object': {
                'Bucket': content['s3']['source']['bucket'],
                'Name': content['s3']['source']['key']
            }
        }
    )
    return response


def lambda_handler(event, context):

    receipt_text = parse_receipt(event)

    response = receipt_text

    # response = put_object(
    #     bucket = event['s3']['target']['bucket'],
    #     key = event['s3']['target']['key'],
    #     data = receipt_text
    # )
    return response

if __name__ == "__main__":
    context = {}

    event = {
        "s3": {
            "source": {
            "bucket": "dbarger-textract-receipts",
            "key": "image/receipt-image.jpg"
            },
            "target": {
            "bucket": "dbarger-textract-receipts",
            "key": "json/receipt-image.json"
            }
        }
    }

    response = lambda_handler(event, context)

    # dict_keys(['ExpenseIndex', 'SummaryFields', 'LineItemGroups'])  

    for document in response['ExpenseDocuments']:
        for item_group in document['LineItemGroups']:
            for items in item_group['LineItems']:
                for expense_field in items['LineItemExpenseFields']:
                    #print(expense_field.get('LabelDetection')['Text'])
                    print(expense_field)
        for summary_field in document['SummaryFields']:
            #print(summary_field.get('LabelDetection')['Text'])
            print(summary_field)


"""
{'Type': {'Text': 'TAX', 'Confidence': 96.87126922607422}, 'LabelDetection': {'Text': 'TAX:', 'Geometry': {'BoundingBox': {'Width': 0.03889123722910881, 'Height': 0.017415843904018402, 'Left': 0.5056823492050171, 'Top': 0.518785297870636}, 'Polygon': [{'X': 0.5058352947235107, 'Y': 0.5188664793968201}, {'X': 0.5445736050605774, 'Y': 0.518785297870636}, {'X': 0.5444642305374146, 'Y': 0.5361225605010986}, {'X': 0.5056823492050171, 'Y': 0.5362011194229126}]}, 'Confidence': 96.83094024658203}, 'ValueDetection': {'Text': '61.32', 'Geometry': {'BoundingBox': {'Width': 0.05108519643545151, 'Height': 0.017450444400310516, 'Left': 0.6363644599914551, 'Top': 0.518485963344574}, 'Polygon': [{'X': 0.6363704800605774, 'Y': 0.518592894077301}, {'X': 0.6873981952667236, 'Y': 0.518485963344574}, {'X': 0.6874496340751648, 'Y': 0.535832941532135}, {'X': 0.6363644599914551, 'Y': 0.5359364151954651}]}, 'Confidence': 96.8567886352539}, 'PageNumber': 1}
"""
