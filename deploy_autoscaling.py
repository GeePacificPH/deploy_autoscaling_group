# Raw Package
from ast import arg
from cgi import test
from curses import echo
import os
import boto3
import sys
from subprocess import run

# Define runtime variables
remote_name_tag = os.getenv('TAG')
remote_port = os.getenv('PORT')
remote_user = os.getenv('USER')
remote_pass = os.getenv('PASS')
remote_key = os.getenv('KEY')
remote_key_file = '/.ssh/id_rsa'
remote_path = os.getenv('TARGET')
local_path = os.getenv('GITHUB_WORKSPACE')+'/'+os.getenv('SOURCE')

# Get instance DNS name info base on name tag
def get_info(instance_name):
    client = boto3.client('ec2',aws_access_key_id=os.getenv('KEY_ID'),aws_secret_access_key=os.getenv('ACCESS_KEY'),region_name=os.getenv('REGION'))
    Myec2 = client.describe_instances(
        Filters=[
        {
            'Name': 'tag:Name',
            'Values': [instance_name]
        },
    ],)
    for field1 in Myec2['Reservations']:
        for field2 in field1['Instances']:
            dns_name = field2['PublicDnsName']
    return(dns_name)

# Sync file
def sync_file_key(r_host):
    args = ['rsync','-vzr','--progress','-e','ssh -o StrictHostKeyChecking=no -i '+remote_key_file+' -p'+remote_port,local_path,remote_user+'@'+r_host+':'+remote_path]
    try:
        p = run(args,capture_output=True)
        if p.returncode!=0:
            raise Exception()
    except:
        sys.stdout.write(str(p.stdout.decode()))
        sys.stderr.write(str(p.stderr.decode()))
        sys.exit(str(p.returncode))
    
def sync_file_pwd(r_host):
    args = ['rsync','-vzr','--progress','-e','sshpass -p '+remote_pass+' ssh -o StrictHostKeyChecking=no -p '+remote_port,local_path,remote_user+'@'+r_host+':'+remote_path]
    try:
        p = run(args,capture_output=True)
        if p.returncode!=0:
            raise Exception() 
    except:
        sys.stdout.write(str(p.stdout.decode()))
        sys.stderr.write(str(p.stderr.decode()))
        sys.exit(str(p.returncode))

# Main component
def main():
    addresses=[get_info(instance_name=remote_name_tag)]
    if remote_key!='':
        f = open(remote_key_file, "w")
        f.write(str(os.getenv('KEY')))
        f.close()
        p = run(['chmod','600',remote_key_file])
        for address in addresses:
            sync_file_key(r_host=address)
    else:
        for address in addresses:
            sync_file_pwd(r_host=address)
    sys.stdout.write("Files synchronization succeed")

main()