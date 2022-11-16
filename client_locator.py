import boto3

class ClientLocator:
    def __init__(self, client):
        self._client = boto3.client(client, region_name="us-east-1")

    def get_client(self):
        return self._client

class EC2Client(ClientLocator):
    def __init__(self):
        super().__init__('ec2')

class S3Client(ClientLocator):
    def __init__(self):
        super().__init__('s3')

class Route53DomainsClient(ClientLocator):
    def __init__(self):
        super().__init__('route53domains')

class SESClient(ClientLocator):
    def __init__(self):
        super().__init__('ses')

class Route53Client(ClientLocator):
    def __init__(self):
        super().__init__('route53')



