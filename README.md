# Serverless S3 To Elasticsearch Ingester
We can load streaming data(say application logs) to Amazon Elasticsearch Service domain from many different sources. Native services like Kinesis & Cloudwatch have built-in support to push data to ES. But services like S3 & DynamoDB can use Lambda function to ingest data to ES.

Follow this article in **[Youtube](https://www.youtube.com/c/ValaxyTechnologies)**

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
yum -y install python-pip zip
pip install virtualenv

# Prepare the log ingestor virtual environment 
mkdir -p /var/s3-to-es && cd /var/s3-to-es
virtualenv /var/s3-to-es
cd /var/s3-to-es && source bin/activate
pip install requests_aws4auth -t .
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

### Setup S3 Event Triggers
we want the code to execute whenever a log file arrives in an S3 bucket:
1. Choose S3\.
1. Choose your bucket\.
1. For **Event type**, choose **PUT**\.
1. For **Prefix**, type `logs/`\.
1. For **Filter pattern**, type `.txt` or `.log`\.
1. Select **Enable trigger**\.
1. Choose **Add**\.

### Configure Lambda Function
1. For **Handler**, type `s3-to-es.lambda_handler`\. This setting tells Lambda the file \(`s3-to-es.py`\) and method \(`lambda_handler`\) that it should execute after a trigger\.
1. For **Code entry type**, choose **Choose a file from Amazon S3**, and Update the URL in the below field\.
1. Choose **Save**\.
1. **If you are running ES in a VPC Access, Make sure your Lambda runs in the same VPC and can reach your ES domain. Otherwise, Lambda cannot ingest data into ES**
- Set the **resource & time limit** based on the size of your log files


### Test the function
- Upload object to S3
- Login to Kibana dashboard or ES Head plugin to check the newly created index & Logs