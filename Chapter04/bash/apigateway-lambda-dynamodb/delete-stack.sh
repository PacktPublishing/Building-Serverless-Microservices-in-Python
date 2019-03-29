#!/bin/sh
# Copyright (c) 2017-2019 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

. ./common-variables.sh

aws cloudformation delete-stack --stack-name $template --region $region --profile $profile
