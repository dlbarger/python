"""
Script:    dynamodb_query.py
Author:    dbarger
Date:      6/24/21

"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

DataSource0 = glueContext.create_dynamic_frame.from_catalog(
    database = "sandbox", 
    table_name = "rockhistory", 
    transformation_ctx = "DataSource0"
)

Transform0 = ApplyMapping.apply(
    frame = DataSource0, mappings = [
        ("index", "long", "index", "long"), 
        ("release_date", "string", "release_date", "string"), 
        ("artist", "string", "artist", "string"), 
        ("popularity", "long", "popularity", "long"), 
        ("length", "double", "length", "double"), 
        ("name", "string", "name", "string"), 
        ("tempo", "double", "tempo", "double"), 
        ("time_signature", "long", "time_signature", "long")], 
    transformation_ctx = "Transform0"
)

# DataSink0 = glueContext.write_dynamic_frame.from_options(
#     frame = Transform0, connection_type = "s3", 
#     format = "json", 
#     connection_options = {"path": "s3://dbarger-public/food/", "partitionKeys": []}, 
#     transformation_ctx = "DataSink0"
# )

DataSink0 = glueContext.write_dynamic_frame.from_options(
    frame = Transform0,
    connection_type = "dynamodb",
    connection_options = {"tableName": "rockhistory-archive"}
)

job.commit()


#glueContext.write_dynamic_frame.from_options(frame =DynamicFrame.fromDF(df, glueContext, "final_df"), connection_type = "dynamodb", connection_options = {"tableName": "pceg_ae_test"})