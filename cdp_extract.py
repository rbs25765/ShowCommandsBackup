from Config_Extract import *
from IP_CMD import IPCmd
import re
from _datetime import datetime
import os


class CdpExtract:

    def __init__(self):
        self.ic = IPCmd()
        self.ce = DeviceConnect()
        self.core_ip = self.ic.core_ip_extract()
        self.device_name = re.compile(r'(?:Device ID:)\s(.+?)(?:\.)')
        self.mgmt_ip_add = re.compile(r'(?:  IP address:) (\d+.\d+.\d+.\d+)')
        self.core_hostname = re.compile(r'(?:hostname\s)(\w+\S\w+.+)')
        self.mgmt_entry_search = re.compile(r'(Entry a.+)')
        self.site_count = 1

    def core_cdp_extract(self, ip):
        # ip_add = ip
        cdp_neighbor_list = [ip]
        cdp_hostname_list = []
        peer_hostname = ""
        i = 0
        out_conf_dict = {}
        flag = False
        try:
            while True:
                ip_add = cdp_neighbor_list[i]
                core_connect = self.ce.dev_connect(ip_add)
                if core_connect is not None:
                    core_connect.enable()
                    core_connect.send_command("terminal length 0")
                    cdp_neighbor_data = core_connect.send_command_timing("show cdp neighbor detail",delay_factor = 20)
                    output_config = self.ce.config_extract(core_connect)
                    out_conf_dict[cdp_neighbor_list[i]] = output_config
                    # print(cdp_neighbor_data)
                    if ip_add == ip:
                        core_hostname_pat = core_connect.send_command("show runn | in hostname", delay_factor=5)
                        core_hostname = self.core_hostname.match(core_hostname_pat).group(1)
                        cdp_hostname_list.append(core_hostname)
                        # print(core_hostname)

                    for line in cdp_neighbor_data.splitlines():
                        if self.device_name.match(line):
                            peer_hostname = self.device_name.match(line).group(1)
                        elif self.mgmt_entry_search.match(line):
                            flag = True
                        elif flag and self.mgmt_ip_add.match(line):
                            neighbor_ip = self.mgmt_ip_add.match(line).group(1)
                            if neighbor_ip not in cdp_neighbor_list and peer_hostname not in cdp_hostname_list:
                                cdp_neighbor_list.append(neighbor_ip)
                                cdp_hostname_list.append(peer_hostname)
                                flag = False
                    print("Site has following inventory ")
                    print(cdp_neighbor_list)
                    print(cdp_hostname_list)
                i += 1
        except IndexError:
            print("CDP Discovery completed {}".format(ip))
            return out_conf_dict

    def device_file_extract(self, final_config_dict, ip):
        if bool(final_config_dict):
            if not os.path.exists('./Output/Site{}'.format(self.site_count)):
                os.mkdir('./Output/Site{}'.format(self.site_count))
            for file, config in final_config_dict.items():
                with open('./Output/Site{}/{}.txt'.format(self.site_count, file), 'a') as f:
                    for item in range(len(config)):
                        f.write(config[item][0])
                        f.write('\n')
                        f.write('\n')
                        f.write(config[item][1])
                        f.write('\n')
                        f.write('\n')
            print("File written to output folder")
        else:
            print("{} Core Device Not accessible".format(ip))

    def core_file_extract(self):
        for core_ip in self.core_ip:
            starttime = datetime.now()
            config_dict = self.core_cdp_extract(core_ip)
            self.device_file_extract(config_dict, core_ip)
            self.site_count += 1
            endtime = datetime.now()
            print("Config Extraction completed {}".format(core_ip))
            print("Execution time {}".format(endtime-starttime))


if __name__ == "__main__":
    cdp = CdpExtract()
    cdp.core_file_extract()




