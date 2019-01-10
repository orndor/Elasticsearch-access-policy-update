'''
    File name: es-access-policy-update.py
    Author: Robo
    Date created: 01/03/2019
    Date last modified: 01/09/2019
    Python Version: 3.6

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
import boto3

# Required function definition for AWS
def lambda_handler(event, context):
# Predefine some variables so we can easily update input parameters.
    key = 'Name'
    value = 'logstash'
    es_domain = 'examplees'
    es_arn = "PASTE ARN BETWEEN QUOTES, EXAMPLE: arn:aws:es:us-east-1:123456789012:domain/examplees/*"
    # Create a boto3 EC2 client
    ec2client = boto3.client('ec2')
    # Create a boto3 Elasticsearch client
    esclient = boto3.client('es')
    # Query AWS for an EC2 instance which matches the predefined tag
    response = ec2client.describe_instances(
        Filters=[
            {
                'Name': 'tag:'+key,
                'Values': [value]
            }
        ]
    )
    if response["Reservations"] != []:
        # Find the public IP address of the instance within the response.
        public_ip = response["Reservations"][0]\
        ["Instances"][0]\
        ["NetworkInterfaces"][0]\
        ["PrivateIpAddresses"][0]\
        ["Association"]\
        ["PublicIp"]
        # Craft a new Policy Document with the new public IP address,
        # and push it to a specific elastic search instance.
        new_access_policy = esclient.update_elasticsearch_domain_config\
        (DomainName=es_domain,AccessPolicies='{"Version":"2012-10-17",' + \
        '"Statement":[{"Effect":"Allow","Principal":{"AWS":"*"},' + \
        "Action":"es:*","Resource":"' + es_arn + '",'\ +
        '"Condition":{"IpAddress":{"aws:SourceIp":["' + public_ip + '"]}}}]}')
    else:
        pass

    return
