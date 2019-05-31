from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from IP_CMD import IPCmd


class DeviceConnect:

    def __init__(self):
        """ These are initializer fields for
            this class"""
        self.device_data = {}
        self.ic = IPCmd()
        self.commands = self.ic.cmd_extract()
        self.device_type = self.ic.device_type_extract()
        self.device_creds = self.ic.device_creds()
        self.device_config = []
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
                print("Connecting to device {}...".format(ip))
                net_con = ConnectHandler(**self.device_data)
                print("Device Connected, executing show commands")
                return net_con
            except NetMikoTimeoutException:
                print(ip+" Device not accessible")
                return None
            except NetMikoAuthenticationException:
                print("Invalid credentials, please modify creds in the file")
                return None

    def config_extract(self, net_connect):

        """ Take the device ip and execute show commands and
            returns a list of command and output"""
        # net_connect = self.dev_connect(ip)
        if net_connect is not None:
            net_connect.enable()
            for cmd in self.commands:
                config_output = net_connect.send_command_timing(cmd, delay_factor=2)
                self.device_config.append((cmd, config_output))
            print("Command Execution Successfully Completed")
            return self.device_config
        else:
            return None

    # def file_saving(self):
    #     for command, data in self.device_config:
    #         with open('./Output/'+self.device_data['ip']+'.txt', 'a+') as f:
    #             f.write('\n')
    #             f.write(command)
    #             f.write('\n')
    #             f.write(data)
    #     print("Writing Completed")


if __name__ == '__main__':

    dc = DeviceConnect()
    net_cons = dc.dev_connect('192.168.2.142')
    dc.config_extract(net_cons)
    print(dc.device_config)
    # dc.file_saving()