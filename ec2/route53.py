
class Route53():
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.route53  """

    def change_cname_record(self, token, domain, zone_id, action):
        print("Performing action {0} on CNAME Record for token {1} for domain {2}".format(action,token, domain))
        return self._client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': action,
                        'ResourceRecordSet': {
                            'Name': token + '._domainkey.' + domain,
                            'Type': 'CNAME',
                            'ResourceRecords' : [
                                {
                                'Value' : token + '.dkim.amazonses.com'
                                }
                            ],
                            'TTL': 60
                        }
                    }
                ]
            }
        )

    def change_mx_record(self, domain, zone_id, action):
        print("Performing action {0} on MX Record for {1}".format(action,domain))
        return self._client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': action,
                        'ResourceRecordSet': {
                            'Name': domain,
                            'Type': 'MX',
                            'ResourceRecords' : [
                                {
                                'Value' : "10 inbound-smtp.us-east-1.amazonaws.com"
                                }
                            ],
                            'TTL': 60
                        }
                    }
                ]
            }
        )

    def list_hosted_zones(self):
        print("Listing Hosted Zones...")
        return self._client.list_hosted_zones()



    def change_site_a_record(self, domain, zone_id, action):
        print("Performing action {0} on A Record for domain {1} zone id {2}".format(action, domain, zone_id))
        return self._client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': action,
                        'ResourceRecordSet': {
                            'Name': domain,
                            'Type': 'A',
                            'AliasTarget': {
                                'HostedZoneId': 'Z3AQBSTGFYJSTF',
                                'DNSName': 's3-website-us-east-1.amazonaws.com.',
                                'EvaluateTargetHealth': True
                            },
                        }
                    }
                ]
            }
        )

