class IPCmd:

    def __init__(self):
        self.core_ip_list = []
        self.cmd_list = []
        self.device_type = ''

    def core_ip_extract(self):
        """To read core device ip from text file
            and returns a list"""
        with open("./Input/device_ip.txt", 'r') as file:
            f = file.read()
            self.core_ip_list = f.strip().splitlines()[1:]
        return self.core_ip_list

    def cmd_extract(self):
        """ Extract device commands from text file
            and returns a list """
        with open("./Input/commands.txt",'r') as file:
            f = file.read()
            self.cmd_list = f.strip().splitlines()[1:]
            return self.cmd_list

    def device_type_extract(self):
        """ Enter choice to connect the device and 
            returns device type """
        print("Press c for Cisco, j for Juniper, h for HP")
        while True:
            choice = input("Enter your Device Choice: ")
            if choice == 'c':
                self.device_type = 'cisco_ios'
                break
            elif choice == 'j':
                self.device_type = 'juniper'
                break
            elif choice == 'h':
                self.device_type = 'hp_procurve'
                break
            else:
                print("Invalid Input! Press c for Cisco, j for Juniper, h for HP! Try again")
        return self.device_type


if __name__ == "__main__":
    ipinfo = IPCmd()
    print(ipinfo.core_ip_extract())
    print(ipinfo.cmd_extract())
    print(ipinfo.device_type_extract())







