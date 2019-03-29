"""
Copyright (c) 2017-2018 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.

API Gateway load testing

Created on 25 Aug 2018

In Shell run
$ sudo pip3 install locustio
$ ./bash/apigateway-lambda-dynamodb/common-variables.sh
$ apiid="$(python  bash/apigateway-lambda-dynamodb/get_apigateway_id.py -e ${template})"
$ locust -f test/locust_test_api.py --host=https://${apiid}.execute-api.${region}.amazonaws.com

Open browser: http://localhost:8089/
"""
import random
from locust import HttpLocust, TaskSet, task

paths = ["/Prod/visits/324?startDate=20171014",
         "/Prod/visits/324",
         "/Prod/visits/320"]


class SimpleLocustTest(TaskSet):

    @task
    def get_something(self):
        index = random.randint(0, len(paths) - 1)
        self.client.get(paths[index])


class LocustTests(HttpLocust):
    task_set = SimpleLocustTest