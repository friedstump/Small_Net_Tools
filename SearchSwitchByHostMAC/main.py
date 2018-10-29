import os
from netmiko import ConnectHandler
from datetime import datetime
import getpass



#Функция поиска MAC


#-----------------------------------------------------------------------

def FindMac(SwitchIP, MacAdd):

    #Цепляемся к текущему свитчу. Ищем MAC
    Sw={"device_type": "cisco_ios", "ip":SwitchIP, "username": UserName, "password":strPass}
    net_connect = ConnectHandler(**Sw)
    strShMacAdd = net_connect.send_command("sh mac address-table address {}".format(MacAdd))

    #65-ый каталист вывод sh mac ad делает несколько иначе чем все остальные свитчи. Поэтому тут дополнительная обработка

    if strShMacAdd.split()[0]=="Legend:":
        print ("Батюшки! Да это же у нас CatOS.65-я как никак")
        strPort = strShMacAdd.split()[-1] #тут хранится порт за которым MAC адрес, посмотрим, есть ли у него CDP соседи!
    else:
        print ("Нормальный каталист")
        strPort = strShMacAdd.split()[16]

    #тут обрабатываем не EtherChannel ли это
    if strPort[0:2]=="Po":              #Если первые два символа Po
        strECNum=strPort[2:]            # обрезаем после Po, что бы получить номер EtherChanel
        print ("Это etherchannel номер {}".format(strECNum))
        strShEtherChannel = net_connect.send_command("sh etherchannel {} summary".format(strECNum))  #дёргаем результат
     
        
        strPort= strShEtherChannel.split()[-7][0:-3]   #берём последний порт в списке, обрезаем его сосстоиние



    print ("АГА! На свитче {} MAC {} видим за портом {}. Поглядим, есть ли там кто по CDP?".format(SwitchIP,MacAdd,strPort))
    strCDPNei = net_connect.send_command("sh cdp neighbors {} detail".format(strPort))
    net_connect.disconnect()


    ####А там то может быть вай-фай-то!!!

    #print (strCDPNei.split())
    ###переделать, на ноль в констисте смотреть некрректно!!!1
    if (strCDPNei=="") or ("Device" not in strCDPNei):   #если CDP ничего не нашёл, значит мы уткнулись в крайний свитч
        print ("Это был последний свитч. Поиск завершён") # И IP его - {}".format(SwitchIP))
        return   SwitchIP    #Валим из рекурсии обратно домой. Возвращем IP свитча на котором остановились
    else:
        strNewSwIP = strCDPNei.split()[8]    #Если что-то нашёл, то ныряем в него
        print ("Оке. Тут у нас ещё  {} Копнём дальше".format(strNewSwIP))
        RecVar=FindMac(strNewSwIP,MacAdd) #вызов самой себя, передаём IP найденного по CDP свитча. При выходе из рекурсии (см.выше) записываем её результат в переменную...

    return RecVar                         #... которую и возвращаем в последствии каждый раз

#-----------------------------------------------------------------------

UserName=input("Please Enter username")
strPass= getpass.getpass('Password:')

HostIP="172.30.242.33" #Задаём изначальный IP. Потом будет браться откуда-то с другого места
start_time = datetime.now()

CoreIP="172.30.21.1"  # Задаём IP коре, откуда начём поиск. Пока тоже ручками.
SwCore ={"device_type": "cisco_ios", "ip":CoreIP, "username":UserName, "password":strPass}

#коннектися к коре
net_connect=ConnectHandler(**SwCore)

strShIPArp = net_connect.send_command("sh ip arp " + HostIP )   # ищем arp на коре
net_connect.disconnect()                                        # нашли всё что надо, можно выйти

lstShIPArp=strShIPArp.split()                                            #вывод  разбиваем пословно и заносим в список



if len(strShIPArp)==0:                                          #вывод пуст
    print  ("Вывод пуст! ARP не найден")
elif lstShIPArp[11]=="Incomplete":                                   #обработка Incomplete
    print ("ARP не найден. Вывод - Incomplete")
else:
    HostMAC=lstShIPArp[11]
    print ("ARP хоста {} - {}".format(HostIP,HostMAC))
    print ("Ищем свитч...")
    print ("IP последнего свитча - {}".format(FindMac(CoreIP,HostMAC)))



end_time = datetime.now()

print ("Время выполнение скрипта {}".format(end_time - start_time))

