
class route53domains():
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.route53domains  """
    
    def check_domain_available(self, domain):
        print("Checking if {0} is available for purchase...".format(domain))
        return self._client.check_domain_availability(
            DomainName=domain
        )

    def check_price(self, tld):
        print("Checking price of TLD {0}".format(tld))
        return self._client.list_prices(
            Tld=tld
        )


    def register_domain(self, info, keep_private=True):
        print("Registering {0}".format(info[0]))
        return self._client.register_domain(
            DomainName=info[0],
            DurationInYears=info[1],
            AutoRenew=info[2],
            AdminContact={
                'FirstName': info[3],
                'LastName': info[4],
                'ContactType': info[5],
                'OrganizationName': info[6],
                'AddressLine1': info[7],
                'AddressLine2': info[8],
                'City': info[9],
                'State': info[10],
                'CountryCode': info[11],
                'ZipCode': info[12],
                'PhoneNumber': info[13],
                'Email': info[14]
            },
            RegistrantContact={
                'FirstName': info[3],
                'LastName': info[4],
                'ContactType': info[5],
                'OrganizationName': info[6],
                'AddressLine1': info[7],
                'AddressLine2': info[8],
                'City': info[9],
                'State': info[10],
                'CountryCode': info[11],
                'ZipCode': info[12],
                'PhoneNumber': info[13],
                'Email': info[14]
            },
            TechContact={
                'FirstName': info[3],
                'LastName': info[4],
                'ContactType': info[5],
                'OrganizationName': info[6],
                'AddressLine1': info[7],
                'AddressLine2': info[8],
                'City': info[9],
                'State': info[10],
                'CountryCode': info[11],
                'ZipCode': info[12],
                'PhoneNumber': info[13],
                'Email': info[14]
            },
            PrivacyProtectAdminContact=keep_private,
            PrivacyProtectRegistrantContact=keep_private,
            PrivacyProtectTechContact=keep_private
        )

    def list_domains(self):
        print("Listing available domains...")
        return self._client.list_domains()

    def list_hosted_zones(self):
        print("Listing Hosted Zones...")
        return self._client.list_hosted_zones()

    