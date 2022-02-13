#!/usr/bin/env python
# This script configures a base Centos 7 VM image with network connectivity and updates Yum Repository
# disabling network manager has been removed. 

import re, os


# gather user input
def userinput():
    userinput.hostname = raw_input("Enter Server Hostname:\n")

    while True:
        userinput.ip = raw_input("Enter IP Address:\n")
        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", userinput.ip):
            print("Invalid IP address, try again!")
        else:
			break

    while True:
        userinput.subnet = raw_input("Enter Subnet Mask:\n")
        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", userinput.subnet):
            print("Invalid subnet, try again!")
        else:
            break

    while True:
        userinput.gateway = raw_input("Enter Gateway:\n")
        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", userinput.gateway):
            print("Invalid gateway, try again!")
        else:
            break

    userinput.dns_server = raw_input("Enter DNS Server name and ip. Example: nameserver 1.1.1.1\n")
userinput()

#stopping NetworkManager
#print "Turning off NetworkManager, Please wait!"

#def networkm():
#    netmoff1 = "systemctl stop NetworkManager"
#    netmoff1_exec = os.popen(netmoff1).read()
#    netmoff2 = "systemctl disable NetworkManager"
#    netmoff2_exec = os.popen(netmoff2).read()
    
#networkm()

# confirm and execute user inputs
def input():
    print ""
    print "Are the Following Paramaters correct:\n"
    print "HOSTNAME: ", userinput.hostname
    print "IP ADDRESS: ", userinput.ip
    print "SUBNET MASK: ", userinput.subnet
    print "GATEWAY: ", userinput.gateway
    print "DNS SERVER: ", userinput.dns_server
    print ""
    while True:
        input.yes = raw_input("type 'y' or 'n': \n")
        if input.yes == 'y':
            # stopping NetworkManager
            print "Turning off NetworkManager, Please wait!"
            netmoff1 = "systemctl stop NetworkManager"
            netmoff1_exec = os.popen(netmoff1).read()
            netmoff2 = "systemctl disable NetworkManager"
            netmoff2_exec = os.popen(netmoff2).read()
            print "Configuring Paramaters!"
            # add Hostname to network file
            input.host = "sudo sed -i '1s/.*/HOSTNAME={}/' /etc/sysconfig/network".format(userinput.hostname)
            input.host_output = os.popen(input.host).read().strip()
            input.host2 = "sudo hostname {}".format(userinput.hostname)
            input.host2_output = os.popen(input.host2).read()
            input.host3 = "sudo sed -i '1s/.*/{}/' /etc/hostname".format(userinput.hostname)
            input.host3_output = os.popen(input.host3).read()

            # add dns entry to resolv.conf file
            input.dns = "sudo sed -i '1s/.*/{}/' /etc/resolv.conf".format(userinput.dns_server)
            input.dns_output = os.popen(input.dns).read().strip()

            # get primary interface name
            input.interface = "sudo ip addr show | grep ^2: | awk '{ print $2 }' | cut -d ':' -f1"
            # ens33 interface name
            input.interface_output = os.popen(input.interface).read().strip()

            # create new UUID
            input.uuid = "sudo uuidgen {}".format(input.interface_output)
            # UUID value (numbers only)
            input.uuid_output = os.popen(input.uuid).read().strip()

            # remove config file
            input.remove_nic = "sudo rm -f /etc/sysconfig/network-scripts/ifcfg-{}".format(input.interface_output)
            input.remove_nic_output = os.popen(input.remove_nic).read().strip()
            # build new network config file
            f = open('/etc/sysconfig/network-scripts/ifcfg-{}'.format(input.interface_output), 'w')
            print >> f, "TYPE=Ethernet"
            print >> f, "PROXY_METHOD=none"
            print >> f, "BROWSER_ONLY=no"
            print >> f, "BOOTPROTO=static"
            print >> f, "DEFROUTE=yes"
            print >> f, "IPV4_FAILURE_FATAL=no"
            print >> f, "IPV6INIT=yes"
            print >> f, "IPV6_AUTOCONF=yes"
            print >> f, "IPV6_DEFROUTE=yes"
            print >> f, "IPV6_FAILURE_FATAL=no"
            print >> f, "IPV6_ADDR_GEN_MODE=stable-privacy"
            print >> f, "NAME={}".format(input.interface_output)
            print >> f, "UUID={}".format(input.uuid_output)
            print >> f, "DEVICE={}".format(input.interface_output)
            print >> f, "NM_CONTROLLED=no"
            print >> f, "ONBOOT=yes"
            print >> f, "IPADDR={}".format(userinput.ip)
            print >> f, "NETMASK={}".format(userinput.subnet)
            print >> f, "GATEWAY={}".format(userinput.gateway)
            f.close()
            # restart network service
            input.network_res = "sudo systemctl restart network"
            input.network_res_output = os.popen(input.network_res).read().strip()
            # up interface
            input.up_nic = "sudo ifup {}".format(input.interface_output)
            input.up_nic_exec = os.popen(input.up_nic).read()

        if input.yes == 'n':
            userinput()

        if not input.yes == 'y' or input.yes == 'n':
            print("Invalid input, 'y' or 'n' only!")
        else:
            break

input()


print "Running Updates, Please wait!"

# updating yum packages
def updates():
    yum_updates = "sudo yum -y update"
    updates_exec = os.popen(yum_updates).read()
    print updates_exec

updates()



print "Setup is Complete!"
