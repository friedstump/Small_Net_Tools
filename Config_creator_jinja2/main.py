

from jinja2 import Environment, FileSystemLoader
import pathlib
import ipaddress

# Directory for final result
DR="C:\\VS_Main\\MCS\\NewSwitches\\SpineConfs"


env = Environment(loader=FileSystemLoader('C:\\VS_Main\\MCS\\NewSwitches'))
template = env.get_template('SpinesConfTemplate.j2') 



# Initial data for manual filling

# Datacenter (can be KO, BE or DP)
DC="KO"
# Name of the first access switch
asw1="nextck96"
# Name of the second access switch
asw2="nextck97"

# Subnets on P2P links between spines and new switches
S1A1Net="172.28.249.116/31"
S2A1Net="172.28.249.118/31"
S1A2Net="172.28.249.120/31"
S2A2Net="172.28.249.122/31"

# Port on Spine switch
Eth1=33
Eth2=34
PC1=100+Eth1
PC2=100+Eth2




fname=DR+"\\"+DC+"_Spines_Conf_"+asw1+"_"+asw2+".ios"


if DC=="BE":
    S1="nspcp3"
    S2="nspcp4"
    area="0.0.3.2"
    SpineAS="3"
elif DC=="KO":
    S1="nspck1"
    S2="nspck2"
    area="0.0.3.1"
    SpineAS="1"
elif DC=="DP":
    S1="nspcp5"
    S2="nspcp6"
    area="0.0.3.3"
    SpineAS="6"   




# Variables which will be used for template
# S1=name of Spine 1
# S2= name of Spine2
# PC1= PortChannel number toward to the first access switch
# PC2= PortChannel number toward to the second  access switch
# E1 = Ethernet interface number toward to the first access switch
# E2=Ethernet interface number toward to the second  access switch


# S1_asw1_IP - IP on Spine1 toward to the first access switch
# S1_asw2_IP - IP on Spine1 toward to the second access switch
# S2_asw1_IP - IP on Spine2 toward to the first access switch
# S2_asw2_IP - IP on Spine2 toward to the second access switch


 
# asw1_S1_IP - IP on the first access switch toward to   Spine1
# asw1_S2_IP - IP on the first access switch toward to   Spine2
# asw2_S1_IP - IP on the second access switch toward to   Spine1
# asw2_S2_IP - IP on the second access switch toward to   Spine2

# asw1_BGP_AS - second octet of  BGP ASN on the first access siwtch 
# asw2_BGP_AS - second octet of  BGP ASN on the second  access siwtch


# ospf_area 


# Dictinary for data rendering 
data={'S1':S1,'S2':S2, 'PC1':PC1, 'PC2':PC2, 'E1':Eth1, 'E2':Eth2,'asw1':asw1,'asw2':asw2,
'S1_asw1_IP':str(ipaddress.ip_network(S1A1Net).network_address),
'S1_asw2_IP':str(ipaddress.ip_network(S1A2Net).network_address),
'S2_asw1_IP':str(ipaddress.ip_network(S2A1Net).network_address),
'S2_asw2_IP':str(ipaddress.ip_network(S2A2Net).network_address),
'asw1_S1_IP':str(ipaddress.ip_network(S1A1Net).broadcast_address),
'asw1_S2_IP':str(ipaddress.ip_network(S2A1Net).broadcast_address),
'asw2_S1_IP':str(ipaddress.ip_network(S1A2Net).broadcast_address),
'asw2_S2_IP':str(ipaddress.ip_network(S2A2Net).broadcast_address),
'ospf_area':area,
'asw1_BGP_AS':"610"+asw1[-2:],
'asw2_BGP_AS':"610"+asw2[-2:],
'SpineAS':SpineAS}



with open (fname, 'w') as f:
    f.write (template.render(data))




