from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from IP_CMD import IPCmd
import logging
import os
# from easygui import passwordbox


class DeviceConnect:

    def __init__(self):
        """ These are initializer fields for
            this class"""
        self.device_data = {}
        self.ic = IPCmd()
        self.commands = self.ic.cmd_extract()
        self.device_type = self.ic.device_type_extract()
        self.device_config = []

    def dev_data(self, ip):
        """ Takes input as ip address and returns
            dev data dictionary as an input for connect handler"""

        self.device_data['ip'] = ip
        self.device_data['username'] = 'cisco'
        # self.device_data['password'] = 'cisco'
        self.device_data['secret'] = 'cisco'
        self.device_data['device_type'] = self.device_type
        # self.device_data['username'] = input("Enter Username: ")
        self.device_data['password'] = input("Enter Password: ")
        # self.device_data['password'] = passwordbox("Enter Password: ")
        # self.device_data['secret'] = passwordbox("Enter Secret: ")
        # self.device_data['secret'] = input("Enter secret: ")
        return self.device_data

    def dev_connect(self, ip):
        """ Takes an ip address as an input and using netmiko
            to connect to device and return handler"""
        self.dev_data(ip)
        i = 1
        while i < 3:
            try:
                print("Connecting to device...")
                net_con = ConnectHandler(**self.device_data)
                # print(self.device_data)
                print("Device Connected, executing show commands")
                return net_con
            except NetMikoTimeoutException:
                print(ip+" Device not accessible")
                return None
            except NetMikoAuthenticationException:
                print("Invalid credentials, please try again")
                self.dev_data(ip)
                i += 1
                if i == 3:
                    logging.warning("You have reached maximum tries, hence existing")
                    return None

    def config_extract(self, ip='192.168.2.14'):
        """ Take the device ip and execute show commands and
            returns a list of command and output"""
        net_connect = self.dev_connect(ip)
        if net_connect is not None:
            net_connect.enable()
            for cmd in self.commands:
                config_output = net_connect.send_command_timing(cmd, delay_factor=2)
                self.device_config.append((cmd, config_output))
            print("Command Execution Successfully Completed")
            print(self.device_config)
            return self.device_config
        else:
            logging.warning("Device {} not accessible or invalid credentials".format(ip))
            return None

    # def file_saving(self):
    #     for command, data in self.device_config:
    #         with open('./Output/'+self.device_data['ip']+'.txt', 'a+') as f:
    #             f.write('\n')
    #             f.write(command)
    #             f.write('\n')
    #             f.write(data)


if __name__ == '__main__':

    dc = DeviceConnect()
    dc.config_extract()
    # dc.file_saving()
    # print(dc.device_config)





