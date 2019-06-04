from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from IP_CMD import IPCmd
import logging


class DeviceConnect:

    def __init__(self):
        """ These are initializer fields for
            this class"""
        self.device_data = {}
        self.ic = IPCmd()
        self.commands = self.ic.cmd_extract()
        self.device_type = self.ic.device_type_extract()
        self.device_creds = self.ic.device_creds()
        self.username = self.device_creds[0]
        self.passwd = self.device_creds[1]
        self.secret = self.device_creds[2]

    def dev_data(self, ip, username, passwd, secret, device_type):
        """ Takes input as ip address, other fields  and returns
            dev data dictionary as an input for connect handler"""

        self.device_data['ip'] = ip
        self.device_data['username'] = username
        self.device_data['password'] = passwd
        self.device_data['secret'] = secret
        self.device_data['device_type'] = device_type

        return self.device_data

    def dev_connect(self, ip):
        """ Takes an ip address as an input and using netmiko
            to connect to device and return handler"""
        if self.device_type is not None:
            self.dev_data(ip, self.username, self.passwd, self.secret, self.device_type)

            try:
                logging.info("Connecting to device {} ...".format(ip))
                print("Connecting to device {}...".format(ip))
                net_con = ConnectHandler(**self.device_data)
                logging.info("Connected to {} successfully ...".format(ip))
                print("Device Connected, executing show commands")
                return net_con
            except NetMikoTimeoutException:
                logging.info("{} Connection Timeout! not accessible...".format(ip))
                print(ip+" Device not accessible")
                return None
            except NetMikoAuthenticationException:
                logging.info("{} Invalid Credentials please modify...".format(ip))
                print("Invalid credentials, please modify creds in the file")
                return None
            except AttributeError:
                print("Device not responding")
                return None


    def config_extract(self, net_connect):

        """ Take the device ip and execute show commands and
            returns a list of command and output"""
        device_config = []
        # net_connect = self.dev_connect(ip)
        if net_connect is not None:
            net_connect.enable()
            for cmd in self.commands:
                config_output = net_connect.send_command_timing(cmd, delay_factor=2)
                device_config.append((cmd, config_output))
            print("Command Execution Successfully Completed")
            return device_config
        else:
            return None

    def config_extract_except(self,net_connect):
        device_config = []
        if net_connect is not None:
            net_connect.enable()
            for cmd in self.commands:
                output = net_connect.send_command_expect(cmd,expect_string=r'>|#|$', delay_factor=4, strip_command=False, strip_prompt=False, max_loops=100)
                device_config.append(output)
            for config in device_config:
                with open ('./Output/{}.txt'.format('device_config'),'a') as f:
                    f.write(output)
            return device_config


if __name__ == '__main__':

    dc = DeviceConnect()
    net_cons = dc.dev_connect('192.168.86.136')
    device = dc.config_extract_except(net_cons)
    print(device)
