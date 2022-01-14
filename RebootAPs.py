#This is used to reboot Class0/Class3 POE devices. Typically APs for my use case. 
#import regex module
import re
#import netmiko for ssh switch connections
import netmiko
from netmiko import *
from netmiko import ConnectHandler
#regex module
from re import *
from time import *

log = open("log.txt","w")

username = "username"
password = "password"
enable = "password"

ips = []

region1 = "ipaddress"
region2 = "ipaddress"

regions = [region1,region2]

for region in regions:
    forthoct = 2
    while (forthoct <100):
        print (f"forth: {forthoct}")
        ips.append(f"{region}{forthoct}")
        print (f"ip: {region}{forthoct}")
        log.write(f"ip: {region}{forthoct}")
        forthoct += 4
print (ips)
#log.write(ips)



for ip in ips:
    dell_sw = {'device_type': 'dell_os10','host': ip,'username': username,'password': password, 'verbose': 'true', 'secret': enable}
    #connect to switch
    
    try:
        ssh = ConnectHandler(**dell_sw)
        
        ssh.enable()
        prompt = ssh.find_prompt()
        #log(f"{ssh.find_prompt()}\n")
        print("Enable")
        log.write(f"{prompt}\n")
        commands = ['do terminal length 0',
                'show power inline']
        results = ssh.send_config_set(commands)
        #ssh.find_prompt()
        #print(results)
        #new line split
        split = results.split("\n")
        #go through each line of output
        log.write(f"{ip}\n")
        for lit in split:
            #find lines with poe class stated
            #APs are typically Class0 or Class3 if they're newer
            pattern = re.compile(".Class0 *|.Class3 *")
            #find lines with sigle digit port number
            pattern2 = re.compile("^Gi1/0/\d\s")
            #do the actual matching
            if pattern.search(lit) and pattern2.search(lit) :
                #if matched split the line
                it = lit.split(" ")
                #remove the Gi for the interface
                print (it[0].replace("Gi",""))
                #log.write(it[0].replace("Gi",""))
                interface = it[0].replace("Gi","")
                turnoffcommands = [
                f'interface gigabitethernet {interface}',
                'power inline never'
                ]
                ssh.send_config_set(turnoffcommands)
                sleep(5)
                turnoncommands = [
                f'interface gigabitethernet {interface}',
                'power inline auto'
                ]
                ssh.send_config_set(turnoncommands)
                
                print (lit)
                log.write(f"{lit}\n")
                #print (lit)
            #match single digit with space after it.
            #pattern = re.compile("^Gi1/0/\d\s")
            #if pattern.search(lit):
            #    print (lit) 
        print("Disconnecting")
        log.write("Disconnecting\n")
        ssh.disconnect()       
    except:
        print(f"Failed connection to: {ip}")
        log.write(f"Failed connection to: {ip}\n")
    
    #else:
     #   print(f"Failed connection to: {ip}")
    



    

        