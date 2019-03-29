#!/bin/sh
# Copyright (c) 2017-2019 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

#endpoint="https://xxxxx.execute-api.eu-west-1.amazonaws.com/Prod/visits/324"
. ./common-variables.sh

endpoint="$(python3 get_apigateway_endpoint.py -e ${template})"
echo ${endpoint}
status_code=$(curl -i -H \"Accept: application/json\" -H \"Content-Type: application/json\" -X GET ${endpoint})
echo "$status_code"
if echo "$status_code" | grep -q "HTTP/1.1 200 OK";
then 
    echo "pass"
    exit 0
else 
    exit 1
fi
