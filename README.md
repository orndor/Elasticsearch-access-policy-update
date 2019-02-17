# Elasticsearch-access-policy-update
![Diagram of Function](https://orndor.com/wp-content/uploads/2019/01/ElasticSearchArch-1.png)
AWS Lambda Function which updates an AWS Elasticsearch Access Policy with logstash spot instance IP

Background: A logstash golden image EC2 spot instance may spin up
spontaneously, and the Elasticsearch server it pipelines logs to needs
to allow it (with a new public IP) to connect.

This function is intended to be used in AWS Lambda to find a specific EC2
spot instance with a specific tag. If this script finds a match, it pulls
the public IP address of that instances and then creates a JSON policy
document. The policy document is then applied to an AWS Elasticsearch domain
to allow the originally matched EC2 instance access.

Here are some other required items within AWS to make this work:

1) A logstash server pushing logs to an AWS managed ES domain.
2) A CloudWatch event, configured as follows:
```json
   {
     "source": [
       "aws.ec2"
     ],
     "detail-type": [
       "EC2 Instance State-change Notification"
     ],
     "detail": {
       "state": [
         "running"
       ]
     }
   }
``` 
3) An IAM role which Lambda assumes and allows the following:
- Allow EC2 Describe Instances
- Allow Update Elasticsearch Domain Config on the required ES domain
