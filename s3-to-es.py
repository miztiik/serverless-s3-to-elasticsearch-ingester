#!/usr/bin/python3
# -*- coding: utf-8 -*-
import boto3
import json
import datetime
import gzip
import urllib
import urllib3
import logging
from requests_aws4auth import AWS4Auth
import requests
from io import BytesIO

"""
Can Override the global variables using Lambda Environment Parameters
"""
globalVars = {}
globalVars['Owner'] = "Mystique"
globalVars['Environment'] = "Prod"
globalVars['awsRegion'] = "eu-central-1"
globalVars['tagName'] = "serverless-s3-to-es-log-ingester"
globalVars['service'] = "es"
globalVars['esIndexPrefix'] = "s3-to-es-"
globalVars['esIndexDocType'] = "s3_to_es_docs"
globalVars['esHosts'] = {
    'test': '',
    'prod': 'https://search-es01-d2jqf4mjsrpehk24xvd6h3w7qm.eu-central-1.es.amazonaws.com'
}

# Initialize Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def indexDocElement(es_Url, awsauth, docData):
    try:
        #headers = { "Content-Type": "application/json" }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        resp = requests.post(es_Url, auth=awsauth,
                             headers=headers, json=docData)
        if resp.status_code == 201:
            logger.info('INFO: Successfully inserted element into ES')
        else:
            logger.error('FAILURE: Unable to index element')
    except Exception as e:
        logger.error('ERROR: {0}'.format(str(e)))
        logger.error('ERROR: Unable to index line:"{0}"'.format(
            str(docData['content'])))
        print(e)


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key,
                       credentials.secret_key,
                       globalVars['awsRegion'],
                       globalVars['service'],
                       session_token=credentials.token
                       )

    logger.info("Received event: " + json.dumps(event, indent=2))

    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(
            event['Records'][0]['s3']['object']['key'])

        # Get documet (obj) form S3
        obj = s3.get_object(Bucket=bucket, Key=key)

    except Exception as e:
        logger.error('ERROR: {0}'.format(str(e)))
        logger.error(
            'ERROR: Unable able to GET object:{0} from S3 Bucket:{1}. Verify object exists.'.format(key, bucket))

    if (key.endswith('.gz')) or (key.endswith('.tar.gz')):
        mycontentzip = gzip.GzipFile(
            fileobj=BytesIO(obj['Body'].read())).read()
        lines = mycontentzip.decode("utf-8").replace("'", '"')
        # print('unzipped file')
    else:
        lines = obj['Body'].read().decode("utf-8").replace("'", '"')

    logger.info('SUCCESS: Retrieved object from S3')

    # Split (S3 object/Log File) by lines
    lines = lines.splitlines()
    if (isinstance(lines, str)):
        lines = [lines]

    # Index each line to ES Domain
    indexName = globalVars['esIndexPrefix'] + \
        str(datetime.date.today().year) + '-' + \
        str(datetime.date.today().month)
    es_Url = globalVars['esHosts'].get(
        'prod') + '/' + indexName + '/' + globalVars['esIndexDocType']

    docData = {}
    docData['objectKey'] = str(key)
    docData['createdDate'] = str(obj['LastModified'])
    docData['content_type'] = str(obj['ContentType'])
    docData['content_length'] = str(obj['ContentLength'])

    for line in lines:
        docData['content'] = str(line)
        indexDocElement(es_Url, awsauth, docData)
    logger.info('File processing comlplete. Check logs for index status')


if __name__ == '__main__':
    lambda_handler(None, None)
