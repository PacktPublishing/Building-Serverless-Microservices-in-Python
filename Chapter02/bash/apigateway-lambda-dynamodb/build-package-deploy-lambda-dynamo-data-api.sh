#!/bin/sh
# Copyright (c) 2017-2019 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# Variables
. ./common-variables.sh

# Run unit tests
./unit-test-lambda.sh

#Create Zip file of your Lambda code (works on Windows and Linux) 
./create-lambda-package.sh

#Package your Serverless Stack using SAM + Cloudformation
aws cloudformation package --template-file $template.yaml \
    --output-template-file ../../package/$template-output.yaml \
    --s3-bucket $bucket --s3-prefix $prefix \
    --region $region --profile $profile

#Deploy your Serverless Stack using SAM + Cloudformation
aws cloudformation deploy --template-file ../../package/$template-output.yaml \
    --stack-name $template --capabilities CAPABILITY_IAM \
    --parameter-overrides AccountId=${aws_account_id} \
    --region $region --profile $profile