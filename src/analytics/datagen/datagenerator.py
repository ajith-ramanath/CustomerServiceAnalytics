import json
import random
import uuid
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

# import the logging library
import logging

# import the boto3 library
import boto3
from botocore.exceptions import ClientError

# create a function that parses json strings and converts them to a dictionary
def parse_json(json_string):
    return json.loads(json_string)

# create a function to create a list of account ids
def create_account_ids():
    account_ids = []
    for i in range(0, 10):
        account_ids.append(str(uuid.uuid4()))
    logging.debug(account_ids)
    return account_ids

# create a function to create a list of site ids for each account
def create_site_ids(account_ids):
    site_ids = {}
    for account_id in account_ids:
        site_ids[account_id] = []
        for i in range(0, 20):
            site_ids[account_id].append(str(uuid.uuid4()))
    logging.debug(site_ids)
    return site_ids

# create a function to create a list of queue ids from a list of site ids
def create_queue_ids(site_ids):
    queue_ids = {}
    for site_id in site_ids:
        queue_ids[site_id] = []
        for i in range(0, 30):
            queue_ids[site_id].append(str(uuid.uuid4()))
    logging.debug(queue_ids)
    return queue_ids

# create a function that generates a dictionary of random data with the schema in ./schema/acceptance.json
def generate_data(schema_file, account_ids, site_ids, queue_ids):
    # create a dictionary to hold the data
    data = {}
    
    # open the schema file and read the contents
    with open(schema_file, 'r') as s:
        schema = parse_json(s.read())
        logging.debug(schema)

    # iterate over the schema and generate random data
    for key, value in schema.items():
        if value == 'integer':
            data[key] = random.randint(1, 20)
        elif value == 'timestamp':
            data[key] = time.strftime('%Y-%m-%d %H:%M:%S')
        elif value == 'boolean':
            data[key] = bool(random.getrandbits(1))
        elif key == 'account_id':
            # random selection from a list of account ids
            data[key] = random.choice(account_ids)
        elif key == 'site_id':
            # random selection from a list of site ids
            data[key] = random.choice(site_ids[data['account_id']])
        elif key == 'queue_id':
            # random selection from a list of queue ids
            data[key] = random.choice(queue_ids[data['site_id']])
        elif key == 'media':
            data[key] = random.choice(['phone', 'chat', 'other'])
        elif key == 'outcome':
            data[key] = random.choice(['finished', 'escalated', 'transferred'])
        elif key == 'environment_name':
            data[key] = random.choice(['acceptance'])
        # uid
        elif key == 'uid':
            data[key] = str(uuid.uuid4())
        else:
            logging.warning("Unknown key or value - %s:%s.", key, value)

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

# function for the thread pool
def execute(args, account_ids, site_ids, queue_ids):
    # create a counter for the number of records sent
    records_sent = 0

    # create a loop that generates data and sends it to AWS Kinesis
    while records_sent < args.records:
        # generate some data
        data = generate_data(
            args.schema_file,
            account_ids,
            site_ids,
            queue_ids
        )

        # send the data
        response = send_data(data, args.stream_name, args.partition_key)

        # log the response
        logging.info(response)

        # increment the counter
        records_sent += 1


# main function
def main():

    # create an argument parser
    parser = argparse.ArgumentParser()

    # add the argument for the number of records to generate
    parser.add_argument('--records', type=int, default=1000)

    # add the argument for the pause between records
    parser.add_argument('--pause', type=int, default=0)

    # add the argument for the log level
    parser.add_argument('--log-level', type=str, default='INFO')

    # add the argument for the log file
    parser.add_argument('--log-file', type=str, default='datagenerator.log')

    # add the argument for the log format
    parser.add_argument('--log-format', type=str, default='%(asctime)s %(thread)d %(levelname)s %(message)s')

    # add the argument for the log date format
    parser.add_argument('--log-date-format', type=str, default='%Y-%m-%d %H:%M:%S')

    # add an argument for stream name
    parser.add_argument('--stream-name', type=str, default='csa-stream')

    # add an argument for partition key
    parser.add_argument('--partition-key', type=str, default='account_id')

    # add an argument for the schema file
    parser.add_argument('--schema-file', type=str, default='./schema/acceptance.json')

    # add an argument for the number of threads
    parser.add_argument('--threads', type=int, default=100)

    # parse the arguments
    args = parser.parse_args()

    # update the code below to use the arguments
    # set the log level
    logging.basicConfig(filename=args.log_file, level=args.log_level, format=args.log_format, datefmt=args.log_date_format)

    # generate a fixed list of account ids
    account_ids = create_account_ids()

    # generate a fixed list of site ids for each account
    site_ids = create_site_ids(account_ids)

    # extract the site ids from the site_ids dictionary
    site_ids_list = [site_id for account_id in site_ids for site_id in site_ids[account_id]]
    logging.debug(site_ids_list)

    # generate a fixed list of queue ids for each site
    queue_ids = create_queue_ids(site_ids_list)

     # Make things concurrent now. Implement thread pool
    futures = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures.append(executor.submit(execute, args, account_ids, site_ids, queue_ids))

# call the main function
if __name__ == '__main__':
    main()