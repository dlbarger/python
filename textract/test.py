"""
Script:  test.py
Test wrapper for textract project.
"""

import src.expense

item = src.expense.Receipt(
    'dbarger-textract-receipts',
    'image/receipt-image.jpg'
)

#print(json.dumps(item.get_receipt('items'),indent=4))
print(item)
