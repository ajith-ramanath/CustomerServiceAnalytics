#!/bin/bash

aws cloudformation create-stack \
--stack-name csa-stack-ajithr-7 \
--template-body file://./setup.yaml \
--parameters ParameterKey=StreamName,ParameterValue=csa-stream-6 \
             ParameterKey=ShardCount,ParameterValue=4 \
             ParameterKey=RetentionPeriodHours,ParameterValue=24