from netmiko import ConnectHandler
from IP_CMD import IPCmd

# from easygui import passwordbox


class DeviceConnect:

    def __init__(self):
        self.device_data = {}

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

    def dev_connect(self):
        net_connect = ConnectHandler(**self.device_data)
        return net_connect

    def print_data(self):
        # print(self.core_ip, self.show_commands)
        ipc = IPCmd()
        device_type = ipc.device_type_extract()
        self.dev_data('192.168.2.131', device_type)
        dev_status = self.dev_connect()
        print(dev_status.find_prompt())


if __name__ == '__main__':

    dc = DeviceConnect()
    dc.print_data()





