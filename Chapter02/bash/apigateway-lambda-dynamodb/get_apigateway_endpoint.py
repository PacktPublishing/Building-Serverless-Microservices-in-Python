"""
Copyright (c) 2017-2019 STARWOLF Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.

Created on 23 Dec 2018
@author: Richard Freeman

This module gets an API Gateway endpoint based on the name
sudo python3.6 -m pip install boto3

"""

import argparse
import logging

import boto3
logging.getLogger('botocore').setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)s %(name)-15s: %(lineno)d %(message)s',
                    level=logging.INFO)
logger.setLevel(logging.INFO)


def get_apigateway_names(endpoint_name):
    client = boto3.client(service_name='apigateway', region_name='eu-west-1')
    apis = client.get_rest_apis()
    for api in apis['items']:
        if api['name'] == endpoint_name:
            api_id = api['id']
            region = 'eu-west-1'
            stage = 'Prod'
            resource = 'visits/324'
            #return F"https://{api_id}.execute-api.{region}.amazonaws.com/{stage}/{resource}"
            return "https://%s.execute-api.%s.amazonaws.com/%s/%s" % (api_id, region, stage, resource)
    return None


def main():
    endpoint_name = "lambda-dynamo-xray"

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpointname", type=str, required=False, help="Path to the endpoint_name")
    args = parser.parse_args()

    if (args.endpointname is not None): endpoint_name = args.endpointname

    apigateway_endpoint = get_apigateway_names(endpoint_name)
    if apigateway_endpoint is not None:
        print(apigateway_endpoint)
        return 0
    else:
        return 1


if __name__ == '__main__':
    main()
