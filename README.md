# CustomerServiceAnalytics

## Introduction

This repository contains a data generator script that creates dummy records mimicking a call centre application. It contains various dimensions related to the service / support request such as account, site, queue, media and outcome. It also generates dummy measures such as wait times for the request to go through. The script sends the data to either AWS Kinesis or MSK that can be configured via the cloud formation templates provided in this repository.

## How to run this script?

  Usage: python datagenerator.py 
                  --stream-type kinesis 
                  --stream-name <stream-name> 
                  --partition-key <partition-key> 
                  --schema-file <schema-file> 
                  --records <number-of-records>"
