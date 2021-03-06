# Raw Package
from ast import arg
from cgi import test
from curses import echo
import os
import sys
import boto3
import paramiko
from subprocess import run

# Define runtime variables
remote_name_tag = os.getenv('TAG')
remote_port = os.getenv('PORT')
remote_user = os.getenv('USER')
remote_pass = os.getenv('PASS')
remote_key = os.getenv('KEY')
remote_key_file = '/.ssh/id_rsa'
remote_path = os.getenv('TARGET')
remote_owner = os.getenv('OWNER')
remote_perm = os.getenv('PERM')
local_path =os.getenv('GITHUB_WORKSPACE')+'/'+os.getenv('SOURCE')
switches =  os.getenv('SWITCHES').split()

# Get instance DNS name info base on name tag
def get_info(instance_name):
    client = boto3.client('ec2',aws_access_key_id=os.getenv('KEY_ID'),aws_secret_access_key=os.getenv('ACCESS_KEY'),region_name=os.getenv('REGION'))
    Myec2 = client.describe_instances(
        Filters=[
        {
            'Name': 'tag:Name',
            'Values': [instance_name]
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ],)
    dns_name=[]
    for field1 in Myec2['Reservations']:
        for field2 in field1['Instances']:
            dns_name = dns_name+[field2['PublicDnsName']]
    return(dns_name)

# Sync file
def sync_file(r_host):
    if remote_key!='':
        f = open(remote_key_file, "w")
        f.write(str(os.getenv('KEY')))
        f.close()
        p = run(['chmod','600',remote_key_file])
        args = ['rsync']+switches+['-e','ssh -o StrictHostKeyChecking=no -i '+remote_key_file+' -p '+remote_port,local_path,remote_user+'@'+r_host+':'+remote_path]
    else:
        args = ['rsync']+switches+['-e','sshpass -p '+remote_pass+' ssh -o StrictHostKeyChecking=no -p '+remote_port,local_path,remote_user+'@'+r_host+':'+remote_path]
    try:
        p = run(args,capture_output=True)
        if p.returncode!=0:
            raise Exception()
    except:
        sys.stdout.write(str(p.stdout.decode()))
        sys.stderr.write(str(p.stderr.decode()))
        sys.exit(str(p.returncode))

# Fix file permission
def set_perm(r_host):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if remote_key!='':
        s.connect(r_host, remote_port, remote_user, key_filename=remote_key_file)
    else:
        s.connect(r_host, remote_port, remote_user, remote_pass)
    command=''
    if remote_perm!='':
        command='sudo chmod -R '+remote_perm+' '+remote_path
        s.exec_command(command)
    if remote_owner!='':
        command='sudo chown -R '+remote_owner+' '+remote_path
        s.exec_command(command)
    s.close()

# Main component
def main():
    addresses=get_info(instance_name=remote_name_tag)
    print(addresses)
    for address in addresses:
        sync_file(r_host=address)
        if remote_owner!='' or remote_perm!='':       
            set_perm(r_host=address)
        sys.stdout.write("Files synchronization succeed on "+str(address)+"\n")

if __name__ == "__main__":
    main()