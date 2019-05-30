from io import StringIO

from paramiko import SSHClient, AutoAddPolicy, AuthenticationException
from paramiko.rsakey import RSAKey

from web.commons import Setting
from web.models.global_config import GlobalConfig


def ssh_ping(hostname, port):
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy)
    try:
        ssh_client.connect(
            hostname,
            port=port,
            username='root',
            pkey=RSAKey.from_private_key(StringIO(Setting.ssh_private_key)))
    except AuthenticationException:
        return False
    ssh_client.close()
    return True


def generate_ssh_key():
    key_obj = StringIO()
    key = RSAKey.generate(2048)
    key.write_private_key(key_obj)
    return key_obj.getvalue(), 'ssh-rsa ' + key.get_base64()


def generate_and_save_ssh_key():
    keys = GlobalConfig.query.filter(GlobalConfig.name.in_(['ssh_private_key', 'ssh_public_key'])).all()
    if len(keys) == 0:
        key_obj = StringIO()
        key = RSAKey.generate(2048)
        key.write_private_key(key_obj)
        private_key, public_key = generate_ssh_key()
        GlobalConfig(name='ssh_private_key', value=private_key, desc='SSH私钥').add()
        GlobalConfig(name='ssh_public_key', value=public_key, desc='SSH公钥').save()
        return key, key.get_base64()
    else:
        raise Exception('Already has ssh key')
