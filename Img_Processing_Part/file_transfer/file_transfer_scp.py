import paramiko
from paramiko import SSHClient
from scp import SCPClient

# ouvrir le port 22 sur le serveur = ufw allow 22/tcp

username = "sdkde"
password = "vmsdkde"
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='192.168.0.19',
                   username=username, password=password)

print(ssh_client)

with SCPClient(ssh_client.get_transport()) as scp:
    scp.put('json_output.json')
