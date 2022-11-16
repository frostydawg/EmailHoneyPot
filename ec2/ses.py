
class SES():
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ses  """

    def verify_identity(self, domain):
        return self._client.verify_domain_identity(
            Domain=domain
        )

    def list_identity(self):
        return self._client.list_identities()

    def verify_dkim(self, domain):
        print("Verifying DKIM...")
        return self._client.verify_domain_dkim(
            Domain=domain
        )

    def create_rule_set(self, name):
        print("Creating Rule Set {0}".format(name))
        return self._client.create_receipt_rule_set(
            RuleSetName=name
        )

    def activate_rule_set(self, name):
        print("Setting {0} as active ruleset".format(name))
        return self._client.set_active_receipt_rule_set(
            RuleSetName=name,
        )

    def create_rule(self, rule_set_name, rule_name, s3_bucket_name, prefix):
        print("Creating Rule for Rule Set:  {0}".format(rule_set_name))
        return self._client.create_receipt_rule(
            RuleSetName=rule_set_name,
            Rule={
                'Recipients': [prefix],
                'Actions': [
                    {
                        'S3Action': {
                            'BucketName': s3_bucket_name,
                            'ObjectKeyPrefix': 'Emails',
                        },
                    },
                ],
                'Enabled': True,
                'Name': rule_name,
                'ScanEnabled': False,
                'TlsPolicy': 'Optional',
            }
        )

    def delete_rule_set(self, rule_set_name):
        print("Deleting Rule Set: {0}".format(rule_set_name))
        return self._client.delete_receipt_rule_set(
            RuleSetName='string'
        )

    def delete_identity(self, identity):
        
        return self._client.delete_identity(
            Identity=identity
        )