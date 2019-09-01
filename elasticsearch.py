'''
    File name: es-access-policy-update.py
    Author: Robo
    Date created: 01/03/2019
    Date last modified: 09/01/2019
    Python Version: 3.7

Background: A logstash golden image EC2 spot instance may spin up
spontaniously, and the Elasticsearch server it pipelines logs to needs
to allow it (with a new public IP) to connect.

This function is intended to be used in AWS Lambda to find a specific EC2
spot instance with a specific tag. If this script finds a match, it pulls
the public IP address of that instances and then creates a JSON policy
document. The policy document is then applied to an AWS Elasticsearch domain
to allow the originally matched EC2 instance access.
'''
# Import the AWS SDK
from boto3 import client, resource

def lambda_handler(event, context):
    # Predefine some variables so we can easily update input parameters.
    es_domain = 'examplees'
    es_arn = "PASTE FULL ESDOMAIN ARN BETWEEN QUOTES"
    # Create a boto3 EC2 resource
    ec2 = resource('ec2')
    # Create a boto3 Elasticsearch client
    esclient = client('es')
    # Use the inbound event data to grab the insance-id; then use that to get the public IP.
    instance = ec2.Instance(event['instance-id'])
    public_ip = instance.public_ip_address

    # Insert the public IP address of the instance into the ES access policy.
        esclient.update_elasticsearch_domain_config(
            DomainName=es_domain, AccessPolicies='{"Version":"2012-10-17",'
            '"Statement":[{"Effect":"Allow","Principal":{"AWS":"*"},'
            '"Action":"es:*","Resource":"' + es_arn + '",'
            '"Condition":{"IpAddress":{"aws:SourceIp":'
            '["' + public_ip + '"]}}}]}'
        )
