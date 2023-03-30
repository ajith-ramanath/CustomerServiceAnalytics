#!/bin/bash

aws cloudformation create-stack \
--stack-name my-msk-stack \
--template-body file://path/to/your/template.yaml \
--parameters ParameterKey=VpcId,ParameterValue=<your_vpc_id> \
                ParameterKey=SubnetIds,ParameterValue=<your_subnet_id_1>,<your_subnet_id_2> \
                ParameterKey=SecurityGroupId,ParameterValue=<your_security_group_id>
