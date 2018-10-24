#!/usr/bin/env python

import boto3
from boto3.dynamodb.conditions import Key, Attr
import pandas as pd
import json

import pprint

pp = pprint.PrettyPrinter(indent=4)

def write_df(TABLE, CATEGORY, DF):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE)
    with table.batch_writer() as batch:
        for item in list(json.loads(DF.T.to_json()).values()):
            batch.put_item(Item=item)
            print(item)


# def read_df(TABLE, CATEGORY):
#
#     response = table.query(
#         KeyConditionExpression=Key('name').eq('user4')
#     )
#     items = response['Items']
#     print(items)
