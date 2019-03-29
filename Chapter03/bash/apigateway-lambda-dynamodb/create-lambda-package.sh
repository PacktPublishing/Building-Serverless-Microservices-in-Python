#!/bin/sh
# Copyright (c) 2017-2019 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

# This script creates a Zip package of the Lambda files

#setup environment variables
. ./common-variables.sh

#Create Lambda package and exclude the tests to reduce package size
(cd ../../lambda_dynamo_read;
mkdir -p ../package/
zip -FSr ../package/"${zip_file}" ${files} -x *tests/*)

