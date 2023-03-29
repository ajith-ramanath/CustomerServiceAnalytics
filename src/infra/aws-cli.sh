#!/bin/bash

aws cloudformation create-stack \
--stack-name csa-stack-ajithr-5 \
--template-body file://./setup.yaml \
--parameters ParameterKey=StreamName,ParameterValue=csa-stream-4 \
             ParameterKey=ShardCount,ParameterValue=4 \
             ParameterKey=RetentionPeriodHours,ParameterValue=24