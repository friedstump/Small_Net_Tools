

#Inputs - VLANID, Subnet/mask, Desctiption
#Results:
#  -  Create a new standart ACL for this VLAN
#  Create SVI on core switch
#  Add VLANs to appropriate switches


#Using "dell_force10" for DELLForce
#Using "arista_eos" for Arista

import os
from netmiko import ConnectHandler
import getpass



# Define IP's of devices

CoreIP="172.30.112.1"
#DellForce10
SrvSw03IP="172.30.112.17"
SrvSw04IP="172.30.112.18"
#Arista
SrvSw07IP="172.30.112.30"
SrvSw08IP="172.30.112.31"



#Trying to connect
#CheckIfCredential is valid
while True:

    try:
        #At this stage Username\Password will be hardcoded
        UserName="ansible_temp"
        strPass="2wsx#EDC"
        
        #UserName=input("Please Enter username ")
        #strPass= getpass.getpass('Password:')
        SwCore ={"device_type": "cisco_ios", "ip":CoreIP, "username":UserName, "password":strPass}
        print ("Trying to connect...")
        net_connect=ConnectHandler(**SwCore)
        print ("Connection to Core Switch is ok with username " + UserName)
        break
    except Exception as e:
        print(str(e) + "\nPlease repeate user\password input")



#While connect to core switch still established we can check that inputed VLAN is valid and do not exist on coreswitch
#ButFirstlt we need to check if it's valid

while True:
    VlanIsCorrect=False
    VLAN_ID=input("Please Enter VLAN_ID")
    try:
        
        
        val = int(VLAN_ID)
        
        
        break
    except ValueError:
        print(VLAN_ID + " is not Integer! Please Enter integer Value")
    

print (VLAN_ID)



'''
VLAN_ID="666"
VlanDescr

SwSrv4NewVlanCommand=[
    "interface Vlan" + str(VLAN_ID),
    "description Python_Cloud",
    "no ip address",
    "tagged TenGigabitEthernet 0/1-7,9-15,17-23,25-31",
    "tagged TenGigabitEthernet 1/1-7,9-15,17-23,25-31",
    "tagged Port-channel 52",
    "no shutdown"
]





AddVlanCommand=["vlan 666", "name PytonVlan"]

###
#SwDell ={"device_type": "arista_eos", "ip":"172.30.112.30", "username":"ansible_temp", "password":"2wsx#EDC"}
SwDell ={"device_type": "dell_os10", "ip":"172.30.112.18", "username":"ansible_temp", "password":"2wsx#EDC"}


net_connect=ConnectHandler(**SwDell)
net_connect.enable()
strShIPArp = net_connect.send_config_set(SwSrv4NewVlanCommand) 

net_connect.disconnect()    

print (strShIPArp)