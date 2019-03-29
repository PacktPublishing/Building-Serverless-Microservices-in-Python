#!/bin/sh
# Copyright (c) 2017-2019 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

#This script gets the API Gateway Id based on the API name ${template}, then runs locust

. ./common-variables.sh
apiid="$(python3 get_apigateway_id.py -e ${template})"
locust -f ../../test/locust_test_api.py --host=https://${apiid}.execute-api.${region}.amazonaws.com
