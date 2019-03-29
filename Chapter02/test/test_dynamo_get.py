"""
Copyright (c) 2017-2019 STARWOLF Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.

Lambda DynamoDB unit tests and mocking

pip install mock

"""

import sys
import unittest
import json

from unittest import mock

from lambda_dynamo_read import lambda_return_dynamo_records as lambda_query_dynamo


class TestIndexGetMethod(unittest.TestCase):
    def setUp(self):
        self.validJsonDataNoStartDate = json.loads('{"httpMethod": "GET","path": "/path/to/resource/324","headers": ' \
                                                   'null} ')
        self.validJsonDataStartDate = json.loads('{"queryStringParameters": {"startDate": "20171013"},' \
                                                 '"httpMethod": "GET","path": "/path/to/resource/324","headers": ' \
                                                 'null} ')
        self.invalidJsonUserIdData = json.loads('{"queryStringParameters": {"startDate": "20171013"},' \
                                                '"httpMethod": "GET","path": "/path/to/resource/324f","headers": ' \
                                                'null} ')
        self.invalidJsonData = "{ invalid JSON request!} "

    def tearDown(self):
        pass

    def test_validparameters_parseparameters_pass(self):
        parameters = lambda_query_dynamo.HttpUtils.parse_parameters(self.validJsonDataStartDate)
        assert parameters['parsedParams']['startDate'] == u'20171013'
        assert parameters['parsedParams']['resource_id'] == u'324'

    def test_emptybody_parsebody_nonebody(self):
        body = lambda_query_dynamo.HttpUtils.parse_body(self.validJsonDataStartDate)
        assert body['body'] is None

    def test_invalidjson_getrecord_notfound404(self):
        result = lambda_query_dynamo.Controller.get_dynamodb_records(self.invalidJsonData)
        assert result['statusCode'] == '404'

    def test_invaliduserid_getrecord_invalididerror(self):
        result = lambda_query_dynamo.Controller.get_dynamodb_records(self.invalidJsonUserIdData)
        assert result['statusCode'] == '404'
        assert json.loads(result['body'])['message'] == "resource_id not a number"

    @mock.patch.object(lambda_query_dynamo.DynamoRepository,
                      "query_by_partition_key",
                       return_value=['item'])
    def test_validid_checkstatus_status200(self, mock_query_by_partition_key):
        result = lambda_query_dynamo.Controller.get_dynamodb_records(self.validJsonDataNoStartDate)
        assert result['statusCode'] == '200'

    @mock.patch.object(lambda_query_dynamo.DynamoRepository,
                       "query_by_partition_key",
                       return_value=['item'])
    def test_validid_getrecords_validparamcall(self, mock_query_by_partition_key):
        lambda_query_dynamo.Controller.get_dynamodb_records(self.validJsonDataNoStartDate)
        mock_query_by_partition_key.assert_called_with(partition_key='EventId',
                                                                partition_value=u'324')

    @mock.patch.object(lambda_query_dynamo.DynamoRepository,
                       "query_by_partition_and_sort_key",
                       return_value=['item'])
    def test_validid_getrecordsdate_validparamcall(self, mock_query_by_partition_and_sort_key):
        lambda_query_dynamo.Controller.get_dynamodb_records(self.validJsonDataStartDate)
        mock_query_by_partition_and_sort_key.assert_called_with(partition_key='EventId',
                                                                partition_value=u'324',
                                                                sort_key='EventDay',
                                                                sort_value=20171013)

    def test_validresponse_httpresponse_valid(self):
        response = lambda_query_dynamo.HttpUtils.respond()
        assert response['statusCode'] == '200'
        assert response['body'] == 'null'

    def test_exception_printexception_printedexception(self):
        assert lambda_query_dynamo.print_exception(Exception('test')) is None

