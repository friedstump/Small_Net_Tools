from netmiko import ConnectHandler
from datetime import datetime
import getpass
from pysnmp.entity.rfc3413.oneliner import cmdgen



Hosts_in_CIDR={
30 : 2,
29 : 6,
28 : 14,
27 : 30,
26 : 62,
25 : 126,
24 : 252,
23 : 510,
22 : '255.255.252.0'
}

### Seeking VLAN on some particular switch. Go to core. Clarify ammount of hosts in this VLAN and amount of possibly free hosts


# функция по анализу арпов
def vlan_analyze (vlanID):
    #так как функция будет вызыватся внутри цикла, важно создать коннекшн к свитчу заранее
    strShRunInt = net_connect.send_command("sh int vlan" + str(vlanID) +" | i Internet")  # ищем arp на коре

    if strShRunInt.split()[0]=="^":
        print ("VLAN ID=" + str(vlanID) + " doesn't routed on core switch")
    else:

        intMask=strShRunInt.split()[-1].split("/")[-1]
        strNumOfHosts=str(Hosts_in_CIDR[int(intMask)])
        strCountOfVlans=dctVlanSum['Vlan'+str(vlanID)]
        strFreeHosts=str(int(strNumOfHosts)-int(strCountOfVlans))
        print ("VLAN ID=" + str(vlanID) + strShRunInt + " Potential number of hosts -  " + strNumOfHosts + ". Count of active ARPs - " + strCountOfVlans + '. Free hosts in VLAN - '+strFreeHosts )


# credentials for switch access
UserName=input("Please Enter username: ")
strPass= getpass.getpass('Password:')
print ("---------------------------------------------------------------")
start_time = datetime.now()

# сначала надо узнать все вланы же
Vlans=[]
# Попробуем SNMP
#вот этот блок я честно слизал с Интернета.
ip='172.30.112.27' # коннектимся например к аристе продовской
community='trYITDjhtf'
value=(1,3,6,1,2,1,17,7,1,4,2,1,3)

generator = cmdgen.CommandGenerator()
comm_data = cmdgen.CommunityData('server', community, 1) # 1 means version SNMP v2c
transport = cmdgen.UdpTransportTarget((ip, 161))

real_fun = getattr(generator, 'nextCmd')
res = (errorIndication, errorStatus, errorIndex, varBinds)\
    = real_fun(comm_data, transport, value)

if not errorIndication is None  or errorStatus is True:
       print ("Error: %s %s %s %s" % res)
else:
    for varBind in varBinds:
        #print(' = '.join([x.prettyPrint() for x in varBind]))
        for x in varBind:
            strx=str(x)
            Vlans.append(int(strx[strx.find('=')+2:]))
    print ("List of VLANS:")
    print (Vlans)



# Спасибо Интернет!




#описываем коре свитч
CoreIP="172.30.115.1"
SwCore ={"device_type": "cisco_ios", "ip":CoreIP, "username":UserName, "password":strPass}





#коннектися к коре
net_connect=ConnectHandler(**SwCore)


strVlanSum=net_connect.send_command("sh arp summ")
#intIndexCount=

lstVlanSum=strVlanSum.split()[int(strVlanSum.split().index('Count'))+1:]

dctVlanSum = dict(zip(lstVlanSum[::2], lstVlanSum[1::2]))


#print (strVlanSum.split()[15:])


any(vlan_analyze(x) for x in Vlans)

net_connect.disconnect()



end_time = datetime.now()

print ("Время выполнение скрипта {}".format(end_time - start_time))
