"""
Script: expense.py
The expense module contains functionality to use AWS Textract service
to parse a receipt image and return the corresponding data structure.
"""

import boto3

textract = boto3.client('textract', region_name = 'us-east-1')

class Receipt():
    """
    Receipt Class
    Interfaces with AWS Textract service to parse data from a receipt image.
    The class integrates with Textract uses boto3.

    Usage:
        Class Variables:
            summary_data: summary receipt data defined by Textract
            items_data: receipt line items defined by Textract
        Public Methods:
            __init__: class constructor that extracts data from image using Textract
            is_receipt: future method to indicate if image is receipt
            get_receipt: get data parsed from image by aggregation type
                raw: direct output from Textract
                summary: Textract SummaryFields json
                items: Texract LineItemExpenseFields json
        Private Methods:
            _parse_image: extract data from receipt image using boto3
            _fetch_summary: extract SummaryFields Textract json objects
            _fetch_items: extract LineItemExpenseFields Textract json objects
    """

    summary_data = {}
    items_data = {}

    def __init__(self, bucket, document) -> None:
        self.bucket = bucket
        self.document = document

        self.raw_data = self._parse_image(
            self.bucket,
            self.document
        )


    def __str__(self) -> str:
        return self.bucket + ':' + self.document


    # Public methods

    def is_receipt(self):
        """Future implementation"""


    def get_receipt(self, data_aggregation):
        """Public method to return parsed data from receipt image"""
        if data_aggregation == 'raw':
            response = self.raw_data

        if data_aggregation == 'summary':
            if self.summary_data:
                response = self.summary_data
            else:
                response = self._fetch_summary(self.raw_data)

        if data_aggregation == 'items':
            if self.items_data:
                response = self.items_data
            else:
                response = self._fetch_items(self.raw_data)

        return response


    # Private method

    def _parse_image(self,bucket,key):
        """Private method to parse receipt image using boto3/Textract."""
        response = textract.analyze_expense(
            Document = {
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            }
        )
        return response


    def _fetch_summary(self, content):
        """Prive method to retreive summary fields from parse receipt data."""
        temp_dict = {}
        data = {}

        key = value = None

        for expense_document in content['ExpenseDocuments']:
            for fields in expense_document['SummaryFields']:
                if 'Type' in fields:
                    key = fields.get('Type')['Text']
                if 'LabelDetection' in fields:
                    key = fields.get('LabelDetection')['Text']
                if 'ValueDetection' in fields:
                    value = fields.get('ValueDetection')['Text']
                if value:
                    temp_dict[key] = value
                    key = value = None

            data['summary'] = temp_dict

        return data


    def _fetch_items(self, content):
        """Private method to retrieve parsed line item data from receipt image."""
        fields_object = {}
        items_list = []
        data = {}

        for expense_document in content['ExpenseDocuments']:
            for item_group in expense_document['LineItemGroups']:
                for items in item_group['LineItems']:
                    for fields in items['LineItemExpenseFields']:
                        fields_object[fields['Type']['Text']] = fields['ValueDetection']['Text']
                    temp_dict = fields_object.copy()
                    items_list.append(temp_dict)

        data['items'] = items_list

        return data
