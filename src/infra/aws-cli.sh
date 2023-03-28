#!/bin/bash

aws cloudformation create-stack \
--stack-name csa-stack-ajithr-3 \
--template-body file://./setup.yaml \
--parameters ParameterKey=StreamName,ParameterValue=csa-stream-2 \
             ParameterKey=ShardCount,ParameterValue=4 \
             ParameterKey=RetentionPeriodHours,ParameterValue=24