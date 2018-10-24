#!/usr/bin/env python

import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('wow_test')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)

#
# with table.batch_writer() as batch:
#     #for item in (df to json as list):
#         batch.put_item(Item=item)
#

from boto3.dynamodb.conditions import Key, Attr

response = table.query(
    KeyConditionExpression=Key('name').eq('Beechworth Pure Honey 1.5kg')
)
items = response['Items']
print(items)
