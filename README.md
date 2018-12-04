# Serverless S3 To Elasticsearch Ingester
We can load streaming data(say application logs) to Amazon Elasticsearch Service domain from many different sources. Native services like Kinesis & Cloudwatch have built-in support to push data to ES. But services like S3 & DynamoDB can use Lambda function to ingest data to ES.

Follow this article in **[Youtube]https://www.youtube.com/c/ValaxyTechnologies)**

![Serverless S3 To Elasticsearch Ingester](https://raw.githubusercontent.com/miztiik/serverless-s3-to-elasticsearch-ingester/master/images/serverless-s3-to-es-ingester-valaxy-miztiik.png)

### Prerequisites
1. S3 Bucket - BucketName: `s3-log-dest`
   - _You will have to create your own bucket and use that name in the instructions_
1. Amazon Elaticsearch Domain [Get help here](https://www.youtube.com/watch?v=cahU_A4c-eE)
1. Amazon Linux with AWS CLI Profile configured
1. Create IAM Role - `s3-to-es-ingestor-bot` [Get help here](https://www.youtube.com/watch?v=5g0Cuq-qKA0&index=11&list=PLxzKY3wu0_FLaF9Xzpyd9p4zRCikkD9lE)
   - Attach following managed permissions - `AWSLambdaExecute`


#### Creating the Lambda Deployment Package
 
 ```sh
 # Install Dependancies
yum -y install zip
pip install virtualenv

# Prepare the log ingestor virtual environment 
mkdir -pr /var/s3-to-es && cd /var/s3-to-es
virtualenv /var/s3-to-es
cd /var/s3-to-es && source bin/activate
pip install requests_aws4auth -t
pip freeze > requirements.txt
# Copy the ingester code to the directory
COPY THE CODE IN THE REPO TO THIS DIRECTORY
# Set the file permission to execute mode
chmod 754 s3-to-es.py

# Package the lambda runtime
zip -r /var/s3-to-es.zip *

# Send the package to S3 Bucket
# aws s3 cp /var/s3-to-es.zip s3://YOUR-BUCKET-NAME/log-ingester/
aws s3 cp /var/s3-to-es.zip s3://s3-log-dest/log-ingester/
```









.decode("utf-8", errors="ignore")
 ```