import requests
import json
import random
username=#Put your user here
EvePass=#Put your pass here
EVEIP=# Put your EVE IP here
login_url = f'https://{EVEIP}/api/auth/login'
cred = '{"username":'+username+',"password":"' + EvePass+'","html5":"-1"}'
headers = {'Accept': 'application/json'}

# ============================= GET SOME COOKIES =======================================
login = requests.post(url=login_url, data=cred, verify=False)
cookies = login.cookies
# =============================  Nodes createion =======================================
for i in range(1,6):
    AristaTmplt={"template":"veos","type":"qemu","count":"1","image":"veos-4.29.2F","name":f"Arista_{i}","icon":"AristaSW.png","uuid":"","cpulimit":"undefined","cpu":"1","ram":"2048","ethernet":"9","firstmac":"","qemu_version":"","qemu_arch":"","qemu_nic":"","qemu_options":"-machine type=pc,accel=kvm -serial mon:stdio -nographic -display none -no-user-config -rtc base=utc -boot order=d","ro_qemu_options":"-machine type=pc,accel=kvm -serial mon:stdio -nographic -display none -no-user-config -rtc base=utc -boot order=d","config":"0","sat":"0","delay":"0","console":"telnet","rdp_user":"","rdp_password":"","left":f"{random.randint(0, 700)}","top":f"{random.randint(0, 500)}","postfix":0}
    AristaTmpltJson=json.dumps(AristaTmplt)
    createNode_url=f'https://{EVEIP}/api/labs/Users/User199/Lab1.unl/nodes'
    create_api = requests.post(url=createNode_url,data=AristaTmpltJson,cookies=cookies,headers=headers, verify=False)
    response =create_api.json()
    device_id = response['data']['id']
    print(f"Created Instance ID is: {device_id}")
# # ============================= Networks (bridges) creation ======================================
createNet_url=f'https://{EVEIP}/api/labs/Users/User199/Lab1.unl/networks'
for i in range (1,4): # по количеству лифоф
    for j in range(1,3): # по количеству спайнов
        NewNetTmplt={"count":1,"name":f"Arista{i}_{j}","type":"bridge","left":0,"top":0,"visibility":1,"postfix":0}
        NewNetTmpltJson=json.dumps(NewNetTmplt)
        create_api = requests.post(url=createNet_url,data=NewNetTmpltJson,cookies=cookies,headers=headers, verify=False)
        response =create_api.json()
        #print ( response)
        device_id = response['data']['id']
        print(f"Created Network ID is: {device_id}")
# # ============================= Links creation ======================================
NetNum=1
for i in range (1,4): # Leaves
    for j in range(1,3): # Spines
        #url for Leaf:
        LeafCurl=f'https://{EVEIP}/api/labs/Users/User199/Lab1.unl/nodes/{i}/interfaces'
        LeafConnData={str(j):NetNum}
        LeafConnDataJson=json.dumps(LeafConnData)
        create_api = requests.put(url=LeafCurl,data=LeafConnDataJson,cookies=cookies,headers=headers, verify=False)        
        #url for spine :
        SpineCurl=f'https://{EVEIP}/api/labs/Users/User199/Lab1.unl/nodes/{j+3}/interfaces'
        SpineConnData={str(i):NetNum}
        SpineConnDataJson=json.dumps(SpineConnData)
        create_api = requests.put(url=SpineCurl,data=SpineConnDataJson,cookies=cookies,headers=headers, verify=False)                       
        NetNum=NetNum+1
# # ==================================================================================
# # ============================= Set bridges invsiible ======================================
# # ==================================================================================
for i in range (1,7):
    NetCurl=f'https://{EVEIP}/api/labs/Users/User199/Lab1.unl/networks/{i}'

    Invis={"visibility":0}
    InvisJson=json.dumps(Invis)
    create_api = requests.put(url=NetCurl,data=InvisJson,cookies=cookies,headers=headers, verify=False)    
