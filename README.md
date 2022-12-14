# EmailHoneyPot

Welcome to EmailHoneyPot v1.0!

<img src="https://raw.githubusercontent.com/frostydawg/EmailHoneyPot/587c6ed1423e9ae8a475a53c93b397a51f4a6369/guide_images/avatar.png" title="" alt="alt text" width="415">

Made by frostydawg

This script was created as a malware research email honey pot tool. It is meant to be a serverless way to obtain malicious emails for malware reverse engineers seeking to analyze samples in the wild. This script has been tested on a fresh Ubuntu 20.04 install



This script assumes you have an AWS account and that you have generated a user in IAM with attached AdministratorAccess permissions. 

For details on how to do that, see this URL (section Creating an administrator IAM user and user group (console)) 

https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html 

It is highly recommended you create a new IAM user and NOT generate a key with your root account.



# Execution

To start, please download dependencies. 

chmod +x setup.sh

./setup.sh

This will install python3, python3-pip, boto3 and the aws cli

It will then prompt you for your AWS Access Key id and the secret access key.

For default region, select "us-east-1" and for default output format select "json"

AWS Access Key ID: your-access-key-id

AWS Secret Access Key: your-secret-access-key

Default region name: us-east-1
 
Default output format: json 


You are now ready to execute the email_honey_pot_deploy.py script!



Simply run

python3 email_honey_pot_deploy.py

Upon executing this script you will have 5 options:



1) Register AWS Route53 Domain for Honeypot
2) Deploy Email Honeypot
3) Generate Honey Emails and post to Pastebin 
4) Delete Email Honeypot
5) Exit



Option 1 - Register AWS Route53 Domain for Honeypot

In order to generate the required AWS infrastructure, you must first register a domain. This domain will be used to host a static S3 website as well as give attackers an address to send emails for your honey pot. 



Option 2 - Deploy Email Honeypot

This will deploy the honeypot infrastructure. This will perform the following actions

????????1) Select your domain 

????????2) Create a domain level identity for the SES service to accept emails ending in your ????????????????chosen domain name

????????3) Add the CNAME records for SES to your DNS hosted zone

????????4) Generate an MX record for your domain to accept emails

????????5) Create an S3 bucket to store your emails

????????6) Create SES receipt rule set with a rule to forward emails to your generated S3 ????????????????bucket

????????7) Create an S3 website with static content 

????????8) Generate an A record to forward traffic from your domain to the static S3 website

????????9) Generate fake email addresses for your domain

????????10) Post those fake email addresses to your Pastebin account



Option 3 - Generate Honey Emails and post to Pastebin

Generate fake emails for your domain and post them to Pastebin (after you have generated your honey pot, you should do this periodically. This will ensure that your emails are eventually picked up by bots/scripts that are scrapping Pastebin for emails to send malware to!)



Option 4 - Delete Email Honeypot

This option will remove all infrastructure created in the Deploy option. It will permanately delete all S3 buckets(and any objects within them), SES rules, and DNS records that were generated by the script. The only remaining artifacts will be your DNS records that were generated when you registered your domain. Depending on how long you set your domain to auto renew, these should remain for 1-2 years if done via the script



Option 5 - Exit

Exit the script





After Deployment

Once you register a domain and deploy your script, you should be all set to receive emails! You can test it by going to a personal email address and sending an email to anything@[yourdomainnamehere]

SES rules are set to accept any emails, so long as the domain is correct.

They will then be forwarded into an S3 bucket created specifically for emails. You can view them by going to the S3 section of the AWS console

![alt text](https://raw.githubusercontent.com/frostydawg/EmailHoneyPot/587c6ed1423e9ae8a475a53c93b397a51f4a6369/guide_images/s3.png)

You should see a bucket that has your selected domain name and ends with "-email-s3"

![alt text](https://raw.githubusercontent.com/frostydawg/EmailHoneyPot/587c6ed1423e9ae8a475a53c93b397a51f4a6369/guide_images/email.png)

You will find a folder titled "Emails" and then there should be emails within that folder anytime someone sends an email to any user @yourdomain

These emails are in MIME format and can easily be parsed out to extract sender, recipient, and attachments (base64 encoded by default in MIME).



After letting this domain sit for a while and periodically posting more email addresses to Pastebin (and anywhere else you like!) you should begin receiving malicious emails to analyze!





TO DO

1) Needs better error handling

2) Needs to post emails to more locations besides pastebin

3) Lambda functions for email parsing

4) Honey Site instead of just static site
