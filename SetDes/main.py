
# Import list of switches from sws.py
from sws import SwitchesRow
import json 
from netmiko import ConnectHandler
import time
from datetime import datetime



# just for coloring
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


Switches=SwitchesRow.split("\n") 



for iSw in Switches:
    swName=iSw.split()[0]
    IP=iSw.split()[1]
    print (bcolors.WARNING+ "Working with " +swName+ "..."+bcolors.ENDC)


    sw={"device_type": "cisco_ios", "ip":IP, "username": "pomazanov", 'allow_agent': 'True', 'use_keys': 'True'}
    net_connect=ConnectHandler(**sw)
    # collecting lldp neigbors
    res=net_connect.send_command("show lldp neighbors | json")
    # JSON deserialization
    jsres=json.loads(res)
    # Going inside...
    lstNb=jsres['TABLE_nbor']['ROW_nbor']
    # New dict with "iface - LLDP_Neig"
    dcLLDP={}

    for i in lstNb:
        iface='Ethernet'+i['l_port_id'][-(len(i['l_port_id'])-3):]
        dcLLDP[iface]=i['chassis_id']

    # collecting current interface descriptions

    res=net_connect.send_command("show int des | json")
    jsres=json.loads(res)
    lstDes=jsres['TABLE_interface']['ROW_interface']

    # working with all this staff
    commands=[]
    # Going through list of description. If interface has not description but this interfaces has LLDP neighbor - depending on entry in LLDP neighbor this will be set up as description
    for i in lstDes:
        if not ("desc" in i):
            if i["interface"] in dcLLDP.keys():
                NewDesc=""
                if "next" in dcLLDP[i["interface"]]:
                    NewDesc="-i- " + dcLLDP[i["interface"]]
                else:
                    NewDesc="-H- " + dcLLDP[i["interface"]]
                commands.append("interface "+i["interface"])
                commands.append("   description "+NewDesc)
                print ("For " + i["interface"]+ " folowwing description will be set: " + NewDesc)


    if len(commands)>1:
        print ("Following command will be udloaded to "+bcolors.FAIL+ swName+bcolors.ENDC)
        for i in commands:
            print (i)
        print (bcolors.FAIL+"Applying commands on "+ swName +"..."+bcolors.ENDC)
        
        res=net_connect.send_config_set(commands)
        print (res)
        net_connect.send_config_set("wr")
        
    else:
        print ("nothing to do with "+bcolors.FAIL+ swName+bcolors.ENDC)



    print (bcolors.FAIL+"Done with "+ swName +". Disconnecting..."+bcolors.ENDC)
    net_connect.disconnect()





print (datetime.now()-start_time)
