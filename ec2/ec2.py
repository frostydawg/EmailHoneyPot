import re
from typing import Type
import requests

class EC2:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ec2  """


    def create_key_pair(self, key_name):
        print("Creating a Key pair with name " + key_name)
        return self._client.create_key_pair(KeyName=key_name)


    def describe_key_pair(self, key_name):
        print("Checking Key pair with name " + key_name)
        return self._client.describe_key_pairs(KeyNames=[key_name])

    def create_security_group(self, group_name, description, vpc_id):
        print('Creating a Security group with name ' + group_name + ' for VPC ' + vpc_id)
        return self._client.create_security_group(
                GroupName=group_name,
                Description=description,
                VpcId=vpc_id
                )
    


    def add_inbound_rule_to_sg(self, security_group_id, type='priv'):
        if type == 'pub':
            range = getip()
        elif type == 'priv':
            range = '0.0.0.0/0'
        self._client.authorize_security_group_ingress(
                GroupId=security_group_id,
                
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 80,
                        'ToPort': 80,
                        'IpRanges': [{'CidrIp': range}]
                        },
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': range}]
                    },
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 0,
                        'ToPort': 65535,
                        'IpRanges': [{'CidrIp': '10.0.0.0/8'}]
                    }
                ]
            )

    def launch_ec2_instance(self, image_id, key_name, min_count, max_count, security_group_id, subnet_id, user_data, device_name='/dev/sda1', instance_type='t2.medium'):
        print('Launching ' + str(min_count) + ' EC2 Instance(s) within subnet ' + subnet_id)
        return self._client.run_instances(
                BlockDeviceMappings=[
        {
            'DeviceName': device_name,
            'Ebs': {
                'DeleteOnTermination': True,
                'VolumeSize': 60,
                'VolumeType': 'gp2'
                
            },
        },
    ],
                ImageId=image_id,
                KeyName=key_name,
                MinCount=min_count,
                MaxCount=max_count,
                InstanceType=instance_type,
                SecurityGroupIds=[security_group_id],
                SubnetId=subnet_id,
                UserData=user_data
                )


    def describe_ec2_instances(self, instance_id):
        print('Describing EC2 Instances...')
        return self._client.describe_instances(
            InstanceIds=[instance_id]
        )

    def reboot_instance(self, instance_id):
        print("Rebooting Instance: " + instance_id)
        return self._client.reboot_instances(
            InstanceIds=[instance_id],
            )

    def modify_ec2_instances(self, instance_id):
        print('Modifying EC2 instancee: ' + instance_id)
        return self._client.modify_instance_attribute(
                InstanceId=instance_id,
                DisableApiTermination={'Value': False}
                )

    def stop_instance(self, instance_id):
        print('Stopping EC2 instance: '+ instance_id)
        return self._client.stop_instances(
                InstanceIds=[instance_id]
                )

    def start_instance(self, instance_id):
        print('Starting EC2 Instance: ' + instance_id)
        return self._client.start_instances(
                InstanceIds=[instance_id]
                )

    def terminate_instance(self, instance_id):
        print('Terminating EC2 Instance: ' + instance_id)
        return self._client.terminate_instances(
                InstanceIds=[instance_id]
                )

    def delete_key_pair(self, key_name):
        print("Deleting Key pair with name " + key_name)
        return self._client.delete_key_pair(KeyName=key_name)


    def create_ami(self, instance_id, ami_name):
        print("Creating AMI From Public Linux Instance")
        return self._client.create_image(
            InstanceId=instance_id, 
            NoReboot=True, 
            Name=ami_name
            )

    def check_ec2_status(self, instance_id):
        print("Checking EC2 Status")
        return self._client.describe_instance_status(
            InstanceIds=[instance_id]
        )

    def check_ami_create_status(self, ami_registered_id):
        print("Checking AMI Creation status")
        return self._client.describe_images(
            ImageIds=[ami_registered_id]
        )

   

def getip():
    try:
        r =requests.get('https://www.checkip.org')
    except:
        print("Could not retrieve IP address. Assigning range 0.0.0.0/0")
        return '0.0.0.0/0'
    result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",r.text)
    if result[0]:
        print("Your External IP is {}".format(result[0]))
        ip = result[0]
        ip_net = ip.split('.')
        for i in range(2,4):
            ip_net[i] = '0'
        sub = '.'.join(ip_net)
        sub = sub + '/16'
        print("Subnet of " + sub + " will have SSH access to EC2 instance")
        return sub
    else:
        print("Could not retrieve IP address. Assigning range 0.0.0.0/0")
        return '0.0.0.0/0'


