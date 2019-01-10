# Elasticsearch-access-policy-update
AWS Lmbda Function which updates an AWS Elasticsearch Access Policy with logstash spot instance IP

Background: A logstash golden image EC2 spot instance may spin up
spontaniously, and the Elasticsearch server it pipelines logs to needs
to allow it (with a new public IP) to connect.

This function is intended to be used in AWS Lambda to find a specific EC2
spot instance with a specific tag. If this script finds a match, it pulls
the public IP address of that instances and then creates a JSON policy
document. The policy document is then applied to an AWS Elasticsearch domain
to allow the originally matched EC2 instance access.
