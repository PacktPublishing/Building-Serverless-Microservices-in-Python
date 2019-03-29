"""
Copyright (c) 2017-2019 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). 
You may not use this file except in compliance with the License. 
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed 
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
express or implied. See the License for the specific language governing 
permissions and limitations under the License.

Created on 8 Jan 2018

@author: Richard Freeman
This package is used to query DynamoDB
"""
import decimal
import json

from boto3 import resource
from boto3.dynamodb.conditions import Key


class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert a DynamoDB item to JSON.
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class DynamoRepository:
    """abstracts all interactions with DynamoDB including the connection and querying of tables
    """
    def __init__(self, target_dynamo_table, region='eu-west-1'):
        self.dynamodb = resource(service_name='dynamodb', region_name=region)
        self.dynamo_table = target_dynamo_table
        self.table = self.dynamodb.Table(self.dynamo_table)

    def query_dynamo_record_by_parition(self, parition_key, parition_value):
        try:
            response = self.table.query(
                KeyConditionExpression=Key(parition_key).eq(parition_value))
            for record in response.get('Items'):
                print(json.dumps(record, cls=DecimalEncoder))
            return

        except Exception as e:
            print('Exception %s type' % str(type(e)))
            print('Exception message: %s ' % str(e))

    def query_dynamo_record_by_parition_sort_key(self, partition_key, partition_value,
                                                 sort_key, sort_value):
        try:
            response = self.table.query(
                KeyConditionExpression=Key(partition_key).eq(partition_value)
                                       & Key(sort_key).gte(sort_value))
            for record in response.get('Items'):
                print(json.dumps(record, cls=DecimalEncoder))
            return

        except Exception as e:
            print('Exception %s type' % str(type(e)))
            print('Exception message: %s ' % str(e))


def main():
    # For manual deployment
    # table_name = 'user-visits'

    # For SAM:
    table_name = 'user-visits-sam'
    partition_key = 'EventId'
    partition_value = '324'
    sort_key = 'EventDay'
    sort_value = 20171001

    dynamo_repo = DynamoRepository(table_name)
    print('Reading all data for partition_key:%s' % partition_value)
    dynamo_repo.query_dynamo_record_by_parition(partition_key, partition_value)

    print('Reading all data for partition_key:%s with date > %d' % (partition_value, sort_value))
    dynamo_repo.query_dynamo_record_by_parition_sort_key(partition_key,
                                                         partition_value,
                                                         sort_key,
                                                         sort_value)


if __name__ == '__main__':
    main()
