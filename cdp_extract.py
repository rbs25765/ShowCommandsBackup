from Config_Extract import *
from IP_CMD import IPCmd
import re


class CdpExtract:

    def __init__(self):
        self.site_layout = {}
        self.ic = IPCmd()
        self.ce = DeviceConnect()
        self.core_ip = self.ic.core_ip_extract()
        self.device_name = re.compile(r'(?:Device ID:)\s(.+)')
        self.mgmt_ip_add = re.compile(r'(?:  IP address:) (\d+.\d+.\d+.\d+)')
        self.core_hostname = re.compile(r'(?:hostname\s)(\w+\S\w+.+)')
        self.mgmt_entry_search = re.compile(r'(Entry a.+)')
        # self.core_hname = ''
        # self.core_ip_extract = ''
        self.site_ip_list = []
        self.site_ips = {}

    def core_cdp_extract(self, ip='192.168.2.142'):
        ip_add = ip
        cdp_neighbor_list = [ip_add]
        cdp_hostname_list = []
        peer_hostname = ""
        i = 0
        out_conf_dict = {}
        try:
            while True:
                ip_add = cdp_neighbor_list[i]
                core_connect = self.ce.dev_connect(ip_add)
                cdp_neighbor_data = core_connect.send_command_timing("show cdp neighbor detail")
                output_config = self.ce.config_extract(core_connect)
                out_conf_dict[ip_add] = output_config

                for line in cdp_neighbor_data.splitlines():
                    if self.device_name.match(line):
                        peer_hostname = self.device_name.match(line).group(1)
                    elif self.mgmt_ip_add.match(line):
                        neighbor_ip = self.mgmt_ip_add.match(line).group(1)
                        if neighbor_ip not in cdp_neighbor_list and peer_hostname not in cdp_hostname_list:
                            cdp_neighbor_list.append(neighbor_ip)
                            cdp_hostname_list.append(peer_hostname)
                i += 1
        except IndexError:
            print("CDP Discovery completed")
        return out_conf_dict

    def file_extract(self):

        final_config = self.core_cdp_extract()

        for file, config in final_config:
            with open('./Output/'+file+'.txt', 'a') as f:
                f.write(config)

    def print_data(self):
        self.file_extract()


cdp = CdpExtract()
cdp.print_data()




