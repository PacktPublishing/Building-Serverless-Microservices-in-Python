#!/bin/sh
# Copyright (c) 2017-2019 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

export profile="demo"
export region="eu-west-1"
# export aws_account_id=$(aws sts get-caller-identity --query 'Account' --profile $profile | tr -d '\"')
export aws_account_id="000000000000"
export template="lambda-dynamo-data-api"
export bucket="testbucket121f"
export prefix="tmp/sam"

# Lambda settings
export zip_file="lambda-dynamo-data-api.zip"
export files="lambda_return_dynamo_records.py"
