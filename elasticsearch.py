'''
    File name: es-access-policy-update.py
    Author: Robo
    Date created: 01/03/2019
    Date last modified: 09/01/2019
    Python Version: 3.7
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
