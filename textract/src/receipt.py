"""
textract.py

"""

import boto3
import json

textract = boto3.client('textract', region_name = 'us-east-1')

class Receipt():

    summaryData = {}
    itemsData = {}

    def __init__(self, bucket, document) -> None:
        self.bucket = bucket
        self.document = document

        self.rawData = self._parseImage(
            self.bucket,
            self.document
        )


    def __str__(self) -> str:
        return(self.bucket + ':' + self.document)


    # Public methods

    def isReceipt(self):
        pass


    def getReceipt(self, format):
        if format == 'raw':
            response = self.rawData

        if format == 'summary':
            if self.summaryData:
                response = self.summaryData
            else:
                response = self._fetchSummary(self.rawData)

        if format == 'items':
            if self.itemsData:
                response = self.itemsData
            else:
                response = self._fetchItems(self.rawData)

        return response


    # Private method

    def _parseImage(self,bucket,key):
        response = textract.analyze_expense(
            Document = {
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            }
        )
        return response


    def _fetchSummary(self, content):
        tempDict = {}
        data = {}

        key = value = None

        for expenseDocument in content['ExpenseDocuments']:
            for fields in expenseDocument['SummaryFields']:
                if 'Type' in fields:
                    key = fields.get('Type')['Text']
                if 'LabelDetection' in fields:
                    key = fields.get('LabelDetection')['Text']
                if 'ValueDetection' in fields:
                    value = fields.get('ValueDetection')['Text']
                if value:
                    tempDict[key] = value
                    key = value = None

            data['summary'] = tempDict

        return data


    def _fetchItems(self, content):

        fieldsObject = {}
        itemsList = []
        data = {}

        for expenseDocument in content['ExpenseDocuments']:
            for itemGroup in expenseDocument['LineItemGroups']:
                for items in itemGroup['LineItems']:
                    for fields in items['LineItemExpenseFields']:
                        fieldsObject[fields['Type']['Text']] = fields['ValueDetection']['Text']
                    tempDict = fieldsObject.copy()
                    itemsList.append(tempDict)

        data['items'] = itemsList

        return data


# Wrapper
if __name__ == "__main__":

    product = Receipt(
        'dbarger-textract-receipts',
        'image/receipt-image.jpg'
    )

    #print(json.dumps(product.getReceipt('raw'),indent=4))
    #print(json.dumps(product.getReceipt('summary'),indent=4))
    print(json.dumps(product.getReceipt('items'),indent=4))

    


