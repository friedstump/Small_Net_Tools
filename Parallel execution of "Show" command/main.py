from netmiko import ConnectHandler

from datetime import datetime
from sws import SwitchesRow
from sws import BESwitches
from sws import DPSwitches
from sws import KOSwitches
from sys import argv
import argparse
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'




start_time = datetime.now()

# Argument parsing
# -c will be used for describing command which should be executed
# -d will be used for chosing particular datacenter
parser = argparse.ArgumentParser(description="Parallel execution of commands")
parser.add_argument("-d",default="All", help="Datacenter selection (KO,DP,BE)")
parser.add_argument("-c", help="Command for execution")
args=parser.parse_args()



# Chosing the Datacenter

if args.d=="KO":
    DC="Korova"
    Switches=KOSwitches.split("\n") 
elif args.d=="DP":
    DC="DATAPRO"
    Switches=DPSwitches.split("\n") 
elif args.d=="BE":
    DC="Berzarina"
    Switches=BESwitches.split("\n") 
else:
    DC="Datacenter has no beeng specified. Command will be executed on all switches"
    Switches=SwitchesRow.split("\n") 

print (DC)




# The function which will be executed in Threading 
def CommandExec (IP, SwName, command):
    sw={"device_type": "cisco_ios", "ip":IP, "username": "pomazanov", 'allow_agent': 'True', 'use_keys': 'True'}
    net_connect=ConnectHandler(**sw)
    res=net_connect.send_command(command)
    net_connect.disconnect()
    return res

  
# If user did not specify "-c" arg then asking him directly which command should be executed
if args.c==None:
    Cmd=input ("Please enter the command to peform: ")
else:
    Cmd=args.c

print (f"Following command will be executed = {Cmd}")



# #################################### Code for Threading Switches:#############################
SwNames=[]
SwIPs=[]
for i in Switches:
    SwNames.append(i.split()[0])
    SwIPs.append(i.split()[1])

# Starting multithreading with 20 workers
with ThreadPoolExecutor(max_workers=20) as executor:
    result=executor.map(CommandExec,SwIPs,SwNames,repeat(Cmd))
    for switch , output in zip(SwNames, result):
       

        print (bcolors.WARNING+"*"+switch+"*"+bcolors.ENDC, ": ", output)

EndTime = datetime.now()
print (EndTime-start_time)
