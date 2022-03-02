import json
import src.expense

item = src.expense.Receipt(
    'dbarger-textract-receipts',
    'image/receipt-image.jpg'
)

print(json.dumps(item.getReceipt('items'),indent=4))