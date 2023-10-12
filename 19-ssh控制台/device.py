class Device(object):
    def __init__(self, ssh, emu=None, dev_info=None, device_manager=None, telnet=None):
        self.ssh = ssh
        self.emu = emu
        self.dev_info = dev_info
        self.device_manager = device_manager
        self.telnet = telnet

    def recv(self):
        try:
            return self.ssh.recv()
        except Exception as e:
            log.error('ssh recv error:{}'.format(e))
            return False

    def send(self, command):
        try:
            self.ssh.send(command)
            return True
        except Exception as e:
            log.error('ssh send error:{}'.format(e))
            return False

    def push(self, local_path, remote_path):
        try:
            self.ssh.push(local_path, remote_path)
            return True
        except Exception as e:
            log.error('ssh push error:{}'.format(e))
            return False

    def send_key(self, key):
        try:
            self.ssh.send_key(key)
            return True
        except Exception as e:
            log.error('ssh send_key error:{}'.format(e))
            return False