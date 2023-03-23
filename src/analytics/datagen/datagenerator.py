import json
import random
import uuid
import time
import argparse

# import the logging library
import logging

# import the boto3 library
import boto3
from botocore.exceptions import ClientError

# create a function that parses json strings and converts them to a dictionary
def parse_json(json_string):
    return json.loads(json_string)

# create a function that generates a dictionary of random data with the schema in ./schema/acceptance.json
def generate_data():
    # create a dictionary to hold the data
    data = {}

    # open the schema file and read the contents
    with open('./schema/acceptance.json', 'r') as schema_file:
        schema = parse_json(schema_file.read())
        logging.debug(schema)

    # iterate over the schema and generate random data
    for key, value in schema.items():
        if value == 'int':
            data[key] = random.randint(0, 100)
        elif value == 'float':
            data[key] = random.random()
        elif value == 'string':
            data[key] = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
        elif value == 'boolean':
            data[key] = random.choice([True, False])
        elif value == 'uid':
            data[key] = str(uuid.uuid4())

    # return the data
    logging.debug(data)
    return data

# create a function that connects to AWS Kinesis and sends the data
def send_data(data, stream_name, partition_key):

    # create a client for the kinesis service
    client = boto3.client('kinesis')
    logging.debug(client)

    # create a json string from the data
    json_string = json.dumps(data)

    response = None
    try:
        response = client.put_record(
            StreamName=stream_name, 
            Data=json_string, 
            PartitionKey=partition_key)
    except ClientError as e:
        print(e)
        logging.exception("Couldn't put record in stream %s.", stream_name)
        raise
    logging.debug(response)
    return response

# create a usage function
def usage():
    print('datagenerator.py --records <number of records> --pause <pause between records>')

# main function
def main():

    # create an argument parser
    parser = argparse.ArgumentParser()

    # add the argument for the number of records to generate
    parser.add_argument('--records', type=int, default=1000)

    # add the argument for the pause between records
    parser.add_argument('--pause', type=int, default=5)

    # add the argument for the log level
    parser.add_argument('--log-level', type=str, default='INFO')

    # add the argument for the log file
    parser.add_argument('--log-file', type=str, default='datagenerator.log')

    # add the argument for the log format
    parser.add_argument('--log-format', type=str, default='%(asctime)s %(levelname)s %(message)s')

    # add the argument for the log date format
    parser.add_argument('--log-date-format', type=str, default='%Y-%m-%d %H:%M:%S')

    # add an argument for stream name
    parser.add_argument('--stream-name', type=str, default='analytics-stream')

    # add an argument for partition key
    parser.add_argument('--partition-key', type=str, default='account_id')

    # add an argument for the schema file
    parser.add_argument('--schema-file', type=str, default='./schema/acceptance.json')

    # parse the arguments
    args = parser.parse_args()

    # update the code below to use the arguments
    # set the log level
    logging.basicConfig(filename=args.log_file, level=args.log_level, format=args.log_format, datefmt=args.log_date_format)

    # create a counter for the number of records sent
    records_sent = 0

    # create a loop that generates data and sends it to AWS Kinesis
    while records_sent < args.records:
        # generate some data
        data = generate_data(
            args.schema_file
        )

        # send the data
        response = send_data(data, args.stream_name, args.partition_key)

        # log the response
        logging.info(response)

        # increment the counter
        records_sent += 1

        # pause for a few seconds
        time.sleep(args.pause)


# call the main function
if __name__ == '__main__':
    main()