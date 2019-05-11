from netmiko import ConnectHandler
from IP_CMD import IPCmd
import os

# from easygui import passwordbox


class DeviceConnect:

    def __init__(self):
        self.device_data = {}
        self.ic = IPCmd()
        self.commands = self.ic.cmd_extract()
        self.device_type = self.ic.device_type_extract()
        self.device_config = []

    def dev_data(self, ip, dev_type):

        self.device_data['ip'] = ip
        self.device_data['username'] = 'cisco'
        self.device_data['password'] = 'cisco'
        self.device_data['secret'] = 'cisco'
        self.device_data['device_type'] = dev_type
        # self.device_data['username'] = input("Enter Username: ")
        # self.device_data['username'] = input("Enter Password: ")
        # self.device_data['password'] = passwordbox("Enter Password: ")
        # self.device_data['secret'] = passwordbox("Enter Secret: ")
        # self.device_data['secret'] = input("Enter secret: ")
        # return self.device_data

    def dev_connect(self):
        print("Connecting to device...")
        net_con = ConnectHandler(**self.device_data)
        return net_con

    def config_extract(self, ip='192.168.2.131'):
        self.dev_data(ip, self.device_type)
        net_connect = self.dev_connect()
        net_connect.enable()
        if net_connect.enable():
            print("Successfully connected, working on capturing configurations")
        for cmd in self.commands:
            config_output = net_connect.send_command_timing(cmd, delay_factor=2)
            self.device_config.append(config_output)
        print("Successfully Completed")
        return self.device_config

    def file_saving(self):
        for data in self.device_config:
            with open('./Output/'+self.device_data['ip']+'.txt','a+') as f:
                f.write(data)


if __name__ == '__main__':

    dc = DeviceConnect()
    dc.config_extract()
    dc.file_saving()
    # print(dc.device_config)





