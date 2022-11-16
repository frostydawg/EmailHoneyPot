import requests
from botocore.exceptions import ClientError
from ec2.vpc import VPC
from ec2.ec2 import EC2
from ec2.s3 import S3
from ec2.ses import SES
from ec2.route53 import Route53
from ec2.route53domains import route53domains
from client_locator import EC2Client
from client_locator import S3Client
from client_locator import Route53DomainsClient
from client_locator import SESClient
from client_locator import Route53Client
from os.path import exists
import json
import sys
import re
import random
from getpass import getpass

def main():
    
    print("Welcome to the Email Honeypot Deployment Program. This program will allow you to deploy \n your own Email Honeypot in AWS")

    print("Select a number from the options menu to begin: ")

    selection = str(input("1) Register AWS Route53 Domain for Honeypot\n2) Deploy Email Honeypot\n3) Generate Honey Emails and post to Pastebin \n4) Delete Email Honeypot\n5) Exit \nInput: "))

    if selection == "1":
        print("Executing Domain Lookup and Execution Script...")
        route53domain = create_route53domains_client()
        print("To start, please enter a domain name to check for availability (include TLD e.g. example.net, example.com, example.co.uk)\nNot including will default to .com")
        print("For a valid list of Top Level Domains (TLDs) see https://data.iana.org/TLD/tlds-alpha-by-domain.txt")
        while True:
            tld = []
            domain_name = input("Input: ")
            tld = re.findall(r'(?:\..+)', domain_name)
            if not tld:
                domain_name +=".com"
                tld.append(".com")
            try:
                result = route53domain.check_domain_available(domain_name) 
                if result['Availability'] == 'AVAILABLE':
                    print("Domain is available for use!")
                    break
                else:
                    print("Domain is NOT available. Please try a different domain")
            except ClientError as c:
                if c.response['Error']['Code'] =='InvalidInput':
                    print("Invalid Input - you entered characters that cannot be in a domain name. See RFC 1035 for valid characters")
                    main()
        price = route53domain.check_price(tld[0][1:])
        agree = input("Cost to register a {0} TLD is ${1:.2f}. You will be charged upon registration by AWS. Continue? (y/n): ".format(tld[0],price['Prices'][0]['RegistrationPrice']['Price']))
        if agree == 'y':
            try:
                print("Registering {}...".format(domain_name))
                register_domain(route53domain, domain_name)
                main()
            except Exception as e:
                print(e)
        else:
            print("Exiting Setup")
            sys.exit(0)

    elif selection ==  "2":
        print("Executing Email Honeypot Deployment Script...")
        route53domain = create_route53domains_client()
        ses = create_ses_client()
        route53 = create_route53client()
        s3 = create_s3_client()
        deploy_honeypot(route53domain, ses, route53, s3)
        sys.exit(1)
    elif selection == "3":
        route53domain = create_route53domains_client()
        domains = route53domain.list_domains()
        domains_available = []
        for each in domains['Domains']:
            print("------------------------")
            print(each['DomainName'] + " is available for use")
            print("------------------------")
            domains_available.append(each['DomainName'])
        selected_domain = input("Please select one of the available domains registered to generate emails from (include TLD e.g. example.com) \nInput: ")
        print("Creating Emails and generating multiple posts to Pastebin. This will get our honeyemails picked up by spammers and malware authors")
        i = 0
        dev_key, username, password =gather_creds()
        while i < 3:
            print("Generating Email Addresses")
            generate_emails(selected_domain)
            print("Posting emails to Pastebin")
            post_emails(dev_key, username, password)
            print("Successfully posted to Pastebin")
            i+=1
        print("Success!")
    elif selection ==  "4":
        print("Executing Email Honeypot Removal Script...")
        route53domain = create_route53domains_client()
        ses = create_ses_client()
        route53 = create_route53client()
        s3 = create_s3_client()
        remove_honeypot(route53domain, ses, route53, s3)
        sys.exit(1)
    elif selection ==  "5":
        print("Quitting. Goodbye")   
    else:
        print("Invalid input")
        sys.exit(2)



def create_route53domains_client():
    route53domains_client = Route53DomainsClient().get_client()

    route53domain = route53domains(route53domains_client)

    return route53domain

def create_route53client():
    route53_client = Route53Client().get_client()

    route53 = Route53(route53_client)

    return route53

def create_ses_client():
    ses_client = SESClient().get_client()

    ses = SES(ses_client)

    return ses

def create_s3_client():
    s3_client = S3Client().get_client()

    s3 = S3(s3_client)

    return s3

def register_domain(route53domain, domain):
    registrant_data = []
    print("To register {0}, we need some information first".format(domain))
    registrant_data.append(domain)
    registrant_data.append(int(input("How many years would you like to register this domain for? \n (The minimum is 1 year, max depends on your chosen TLD. \n This program will limit your selection to 2 years max): ")))
    if registrant_data[1] < 1 or registrant_data[1] > 2:
        print("Invalid number. Defaulting to 1 year")
        registrant_data[1] = 1
    registrant_data.append(input("Auto Renew domain registration? (True or False - case sensitive. Defaults to False): "))
    if registrant_data[2] == "True":
        registrant_data[2] = True
    else:
        registrant_data[2] = False
    registrant_data.append(input("First Name: "))
    registrant_data.append(input("Last Name: "))
    registrant_data.append(input("Contact Type (Valid Selections: 'PERSON'|'COMPANY'|'ASSOCIATION'|'PUBLIC_BODY'|'RESELLER' [Case Sensitive!]): "))
    if registrant_data[5] != "PERSON":
        registrant_data.append(input("You have selected an option other than PERSON.\nPlease provide an Organization Name: "))
    else:
        registrant_data.append("")
    registrant_data.append(input("Address Line 1: "))
    registrant_data.append(input("Address Line 2 (leave blank if none): "))
    registrant_data.append(input("City: "))
    registrant_data.append(input("State: "))
    registrant_data.append(input("Country Code \n(2 letter alphabetical. See https://www.aresearchguide.com/countrycode1.html for listing): "))
    registrant_data.append(input("Zip Code: "))
    registrant_data.append(input("Phone Number (create a Google Phone number if you do not want to use your own)\nPhone number MUST be in +999.12345678 format!: "))
    registrant_data.append(input("Email: "))

    for each in registrant_data:
        print(each)
    print("Register {0} with above information? (y/n)".format(registrant_data[0]))
    confirm = input("Input: ")
    if confirm == 'y':
        result = route53domain.register_domain(registrant_data)
    else:
        print("Returning to main menu...")
        main()
    print("Domain is being registered.\nThis may take a while before your domain will be ready to use!")

def create_s3_email_bucket(s3, s3_bucket_name):

    s3_response = s3.create_s3_bucket(s3_bucket_name)

    s3_policy_resource_name = "arn:aws:s3:::" + s3_bucket_name + "/*"

    s3_policy_id = s3_bucket_name + str(random.randrange(10000))

    Policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowSESPuts",
            "Effect": "Allow",
            "Principal": {
                "Service": "ses.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": s3_policy_resource_name 
        }
    ]
}
    
    s3_bucket_policy = json.dumps(Policy)
    s3.update_policy(s3_bucket_name, s3_bucket_policy)
   
    
def deploy_honeypot(route53domain, ses, route53, s3):
    print("Welcome to the Honeypot Deployment!\nFirst we need to select an available domain from your list of available domains")
    domains = route53domain.list_domains()
    domains_available = []
    for each in domains['Domains']:
        print("------------------------")
        print(each['DomainName'] + " is available for use")
        print("------------------------")
        domains_available.append(each['DomainName'])
    print("If you do not see a recently registered domain, please wait. It may still be pending registration with Amazon (May take 10 minutes or longer. Come back later!)")
    print("Which domain would you like to use? (Type full name including TLD (.com, .net, etc)")
    while True:
        selected_domain = input("Input: ")
        if selected_domain not in domains_available:
            print("Invalid Domain. Please check spelling and try again")
        else:
            break
    print("Domain {0} selected. Time to set up the honeypot!".format(selected_domain))
    print("------------------------")
    print("Verifying Domain Identity for {0}".format(selected_domain))
    test_identity = ses.list_identity()
    if selected_domain not in test_identity:
        print("Identity not yet verified for this domain. Verifying....")
        ses.verify_identity(selected_domain)
        print("Identity Verification may take a while. Continuing setup...")
    response = ses.verify_dkim(selected_domain)
    tokens = response['DkimTokens']
    zones = route53.list_hosted_zones()
    zone_id = ''
    for zone in zones['HostedZones']:
        if zone['Name'][:-1] == selected_domain:
            zone_id = zone['Id']
            print("Found Id {0} for zone {1}".format(zone['Id'], zone['Name'][:-1]))
            break
        else:
            continue
    zone_id = re.search("(?<=\/hostedzone\/).*", zone_id)
    print(zone_id.group(0))
    for token in tokens:
        try:
            route53.change_cname_record(token, selected_domain, zone_id.group(0), 'CREATE')
        except ClientError as c:
            if c.response['Error']['Code'] == 'InvalidChangeBatch':
                print(token + " record already exists. Continuing")
    print("Successfully created CNAME Records!")
    try:
        route53.change_mx_record(selected_domain, zone_id.group(0), 'CREATE')
    except ClientError as c:
        if c.response['Error']['Code'] == 'InvalidChangeBatch':
            print(selected_domain + " MX record already exists. Continuing")
    try:
        create_s3_email_bucket(s3, selected_domain + "-email-s3")
        print("S3 Bucket Created with name: " + selected_domain +"-email-s3")
    except Exception as e:
        print("Error creating S3 Bucket")
        print(e)
    try:
        ses.create_rule_set(selected_domain + "-ruleset")
        ses.activate_rule_set(selected_domain + "-ruleset")
    except ClientError as c:
        if c.response['Error']['Code'] == "AlreadyExists":
            print("Rulset already exists. Continuing")

    try:
        ses.create_rule(selected_domain + "-ruleset", selected_domain + "-email-rule", selected_domain + "-email-s3", selected_domain)
    except ClientError as c:
        if c.response['Error']['Code'] == "AlreadyExists":
            print("Ruleset Already exists. Continuing")
    except Exception as e:
        print("Error")
        print(e)

    print("Creating S3 Bucket Website for {0}".format(selected_domain))
    try:
        create_site(s3, selected_domain)
    except Exception as e:
        print(e)

    print("Site Created. Creating A record to forward traffic to {0} to S3 bucket".format(selected_domain))
    
    try:
        route53.change_site_a_record(selected_domain, zone_id.group(0), 'CREATE')
        print("Successfully created S3 Site A Record!")
        print("You should now be able to visit {0} and see a \"Site Under Construction\" page!".format(selected_domain))
    except Exception as e:
        print(e)



    print("Creating Emails and generating multiple posts to Pastebin. This will get our honeyemails picked up by spammers and malware authors")
    i = 0
    dev_key, username, password = gather_creds()
    while i < 3:
        print("Generating Email Addresses")
        generate_emails(selected_domain)
        print("Posting emails to Pastebin")
        post_emails(dev_key, username, password)
        print("Successfully posted to Pastebin")
        i+=1
   





def create_site(s3, selected_domain):
    policy = 'public-read'
    s3.create_s3_bucket(selected_domain, policy)

    s3.put_bucket_site(selected_domain)

    f = open("site/index.html", "r")
    index = f.read()
    f.close()

    s3.put_object_to_site(selected_domain, index, 'index.html')

    f = open("site/error.html", "r")
    error = f.read()
    f.close()

    s3.put_object_to_site(selected_domain, error, 'error.html')    

    print("Successfully added content to S3 Site")

    






def generate_emails(domain):

    f = open("names/accounts.txt", "r")
    accounts = f.read().splitlines()
    f.close()

    emails = []
    for account in accounts:
        emails.append(account + "@" + domain)

    f = open("names/first.txt", "r")
    first = f.read().splitlines()
    f.close()
    
    f = open("names/last.txt", "r")
    last = f.read().splitlines()
    f.close()

    for x in range(1000):
        emails.append(random.choice(first) + "." + random.choice(last) + "@" + domain)


    with open('names/emails.txt', 'w') as f:
        for each in emails:
            f.write(each)
            f.write('\n')

    f.close()

    print("Successfully wrote emails to names/emails.txt")

def gather_creds():
    print("Please provide a Dev API key for Pastebin \n(It is strongly advised to create a new account not associated to you)")
    dev_key = input("Input: ")

    print("Please provide Pastebin Account User name")
    username = input("Input: ")

    print("Please provide Pastebin Password")
    password = getpass("Input: ")
    return dev_key, username, password

def post_emails(dev_key, username, password):
    
    title = "email dump"

    f = open("names/emails.txt", 'r')
    emails = f.read()
    f.close()
    
    login_data = {
        'api_dev_key': dev_key,
        'api_user_name': username,
        'api_user_password': password
    }    

    data = {
        'api_option': 'paste',
        'api_dev_key': dev_key,
        'api_paste_code': emails,
        'api_paste_name': title,
        'api_paste_expire_data': 'N',
        'api_user_key': None,
        'api_paste_format': 'xml'
    }
    try:
        login = requests.post("https://pastebin.com/api/api_login.php", data=login_data)

        print("Login Status: ", login.status_code if login.status_code!= 200 else "OK/200")

        print("User token: ", login.text)

        data['api_user_key'] = login.text

        r = requests.post("https://pastebin.com/api/api_post.php", data=data)        

        print("Login Status: ", r.status_code if login.status_code!= 200 else "OK/200")
        
        print("Paste URL:", r.text)
    except Exception as e:
        print("Error ")
        print(e)
        print("Failed to post. You can always come back and try again later by selecting option \"3) Generate Honey Emails and post to Pastebin\" on the main menu")

def remove_honeypot(route53domain, ses, route53, s3):
    print("Welcome to HoneyPot Removal Script. This will remove your honeypot infrastructure")
    domains = route53domain.list_domains()
    domains_available = []
    for each in domains['Domains']:
        print("------------------------")
        print(each['DomainName'] + " registered")
        print("------------------------")
        domains_available.append(each['DomainName'])
    print("Which domain listed was used to create your honeypot? (Type full name including TLD (.com, .net, etc)")
    while True:
        selected_domain = input("Input: ")
        if selected_domain not in domains_available:
            print("Invalid Domain. Please check spelling and try again")
        else:
            break
    print("Domain {0} selected. Time to remove the honeypot!".format(selected_domain))

    
    try:
        objects = s3.list_s3_objects(selected_domain)
        for key in objects['Contents']:
            s3.delete_s3_object(selected_domain, key['Key'])
    except Exception as e:
        print(e)

    
    try:
        objects = s3.list_s3_objects(selected_domain + '-email-s3')
        for key in objects['Contents']:
            s3.delete_s3_object(selected_domain + '-email-s3', key['Key'])
    except Exception as e:
        print(e)

    try:
        s3.delete_bucket(selected_domain + "-email-s3")
        s3.delete_bucket(selected_domain)
        print("Deleted S3 buckets and contents")
    except Exception as e:
        print(e)
    

    try:
        ses.delete_rule_set(selected_domain + "-ruleset")
    except Exception as e:
        print(e)

    try:
        ses.delete_identity(selected_domain)
    except Exception as e:
        print(e)

    zones = route53.list_hosted_zones()
    zone_id = ''
    for zone in zones['HostedZones']:
        if zone['Name'][:-1] == selected_domain:
            zone_id = zone['Id']
            print("Found Id {0} for zone {1}".format(zone['Id'], zone['Name'][:-1]))
            break
        else:
            continue
    zone_id = re.search("(?<=\/hostedzone\/).*", zone_id)
    print(zone_id.group(0))

    zone = zone_id.group(0)
    
    try:
        route53.change_mx_record(selected_domain, zone_id.group(0), 'DELETE')
    except Exception as e:
        print(e)
    tokens=[]
    try:
        response = ses.verify_dkim(selected_domain)
        tokens = response['DkimTokens']
    except Exception as e:
        print(e)
    for token in tokens:
        try:
            route53.change_cname_record(token, selected_domain, zone_id.group(0), 'DELETE')
        except ClientError as c:
            if c.response['Error']['Code'] == 'InvalidChangeBatch':
                print(token + " not found Continuing")
    try:
        route53.change_site_a_record(selected_domain, zone_id.group(0), 'DELETE')
    except Exception as e:
        print(e)
        
    
    print("Deletion Complete. Your domain will remain active until the expiration date (usually 1-2 years after purchase)")
    


if __name__ == '__main__':
    main()    

