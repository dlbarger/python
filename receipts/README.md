# H1 Receipt Capture Prototype

# H2 Introduction

# H2 Architecture

# H2 Prequisites 

# H2 Deployment

aws cloudformation create-stack --stack-name textract-receipts --template-body file://cfn-textract-receipts.yml --parameters ParameterKey=ReceiptBucket,ParameterValue=textract-receipts ParameterKey=SourceCodeBucket,ParameterValue=dbarger-source-code ParameterKey=SourceCodeKey,ParameterValue=python/textract-receipts/main.zip