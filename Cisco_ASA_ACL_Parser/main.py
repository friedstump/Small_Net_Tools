
fObjects=open("Objects.txt","r")
dObjects={}
# собираем все объекты
lVal=[]
strName="First element"
for line in fObjects:
    
    if "object network" in line:
       dObjects[strName]=lVal
       strName=str(line)[15:-1]
       lVal=[]
    else:
        lVal.append(str(line.rstrip()))
dObjects[strName]=lVal

fObjects.close()


#Собираем все объектные группы
fObjectGroups=open("Object-g-n.txt","r")
dObjectsGN={}

lVal=[]
strName="First element"
for line in fObjectGroups:
    
    if "object-group network" in line:
       dObjectsGN[strName]=lVal
       strName=str(line)[21:-1]
       lVal=[]
    else:
        lVal.append(str(line.rstrip()))
dObjectsGN[strName]=lVal

fObjectGroups.close()


#Собираем все сервисные группы

fObjectGroupsSer=open("Object-g-s.txt","r")
dObjectsGS={}

lVal=[]
strName="First element"
for line in fObjectGroupsSer:
    
    if "object-group service" in line:
       dObjectsGS[strName]=lVal
       strName=str(line)[21:-1]
       lVal=[]
    else:
        lVal.append(str(line.rstrip()))
dObjectsGS[strName]=lVal

fObjectGroupsSer.close()





#парсим ACL VTBUASTRIA, так как оттуда надо копировать всё. 
# нам надо получить используемые там группы

fAclVTABAUS=open("VTBAUSTRIA-in-acl.txt")
usedServices={} # формируем используемые сервисы 
usedOG={} # формируем используемые группы 
for line in fAclVTABAUS:
    if not ("remark" in line):
        lLine=line.split()
        serv=lLine[5]
        usedServices[serv]=dObjectsGS[serv]
        if not ("any4 any4" in line):
            src=lLine[7]
            dst=lLine[9]
            usedOG[src]=dObjectsGN[src]
            usedOG[dst]=dObjectsGN[dst]


# оказывается нутри объектных групп могут быть другие групп. Соберём и их
usedOG2={}
for iKey in usedOG.keys():
    for iVal in usedOG[iKey]:
        if "group-object" in iVal:
            usedOG2[str(iVal).split()[1]]=dObjectsGN[str(iVal).split()[1]]


#теперь у нас есть два словаря объектных групп которые могут быть задействованы
# for iKey in usedOG2.keys():
#     for iVal in usedOG2[iKey]:
#         print (iVal)
#print (usedOG["S_10.16.4.0s23_VTBAUSTRIA_USER_ACCESS"])

usedOGGeneral={**usedOG, **usedOG2}

#теперь надо понять что конфигурируем из используемых объектов
usedObjects={}

for iKey in usedOGGeneral.keys():
    for iVal in usedOGGeneral[iKey]:
        if (not "description" in iVal) and (not "group-object" in iVal) :
            if  iVal.split()[1]!="host":
                objName=iVal.split()[2]
            
                usedObjects[objName]=dObjects[objName]
            else:
                print ("Object with 'host' inside - ", iKey)


#print  (dObjects)

#Объекты - usedObjects

#Группы - usedOGGeneral
# Сервисы -  usedServices

#Делаем конфигурацию используемых объектов

fAutConfig=open("objects_for_VTBAUSTRIA_ACL.iso","w")
for i in usedObjects.keys():
    fAutConfig.write ("object network ")
    fAutConfig.write (i)
    fAutConfig.write ("\n")
    for j in usedObjects[i]:
        fAutConfig.write (j)
        fAutConfig.write ("\n")
fAutConfig.write ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
fAutConfig.write ("!!!!!!!!!!!!!!! Config groups !!!!!!!!!!!!!!!!!!\n")
fAutConfig.write ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
#Делаем конфигурацию для используемых групп
for i in usedOGGeneral.keys():
    fAutConfig.write ("object-group network ")
    fAutConfig.write (i)
    fAutConfig.write ("\n")
    for j in usedOGGeneral[i]:
        fAutConfig.write (j)
        fAutConfig.write ("\n")

fAutConfig.write ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
fAutConfig.write ("!!!!!!!!!!!!!!! Config services !!!!!!!!!!!!!!!!!!\n")
fAutConfig.write ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")           
#Делаем конфигурацию для используемых сервисов
for i in usedServices.keys():
    fAutConfig.write ("object-group service ")
    fAutConfig.write (i)
    fAutConfig.write ("\n")
    for j in usedServices[i]:
        fAutConfig.write (j)
        fAutConfig.write ("\n")

fAutConfig.close()

### надо написать кусок кода который спарсит все группы, содержащие 
# сначала пробежим по объектам, может кто из них присуствует
lAusObjects=[]
for iKey in dObjects.keys():
    for iVal in dObjects[iKey]:
        if "10.196" in iVal or "10.144" in iVal or "10.145" in iVal or  "10.146" in iVal or  "10.147" in iVal or  "10.16" in iVal or  "10.17" in iVal or  "10.18" in iVal or  "10.19" in iVal or  "172.16.16" in iVal:
            lAusObjects.append(iKey)


lAusObjectGroups=[]

#пробежимся по словарю объектных групп и если такоевые имеются занесём их в наш лист

for iKey in dObjectsGN.keys():
    for iVal in dObjectsGN[iKey]:
        #if iVal in lAusObjects:
        if iVal.split()[-1] in lAusObjects:
            lAusObjectGroups.append(iKey)
lAusObjectGroupsSet=set(lAusObjectGroups)

   
    #if iKey in dObjectsGN:
     #   print (iKey)


fAclInside=open("inside-in-acl.txt")
fNewAclInside=open("NEW_INSIDE_ACL.ios", "w")
for line in fAclInside:
    if "remark" in line:
        strRemark=str(line)
    for i in lAusObjects:
        if i in line:
            fNewAclInside.write(strRemark)
            #fNewAclInside.write("\n")
            fNewAclInside.write(line)
            #fNewAclInside.write("\n")

            ### У нас появилась строчка с ACL-кой можно применить старый алгоритм, конечно
            # который применяли для но чёто как то сложно,
            # я не умею программить, сохраню ка я лучше его ещё в файл а потом распарсю


    for i in  lAusObjectGroupsSet:
        if i in line:
            fNewAclInside.write(strRemark)
            #fNewAclInside.write("\n")
            fNewAclInside.write(line)
            #fNewAclInside.write("\n")
      

fNewAclInside.close()
##########################################
#### А теперь тупо делаем тоже самое что делали для VTBAUSTRIA
################################




#парсим ACL NEW-inside-in, так как оттуда надо копировать всё. 
# нам надо получить используемые там группы

fAclNewInside=open("NEW_INSIDE_ACL.ios")
usedServices={} # формируем используемые сервисы 
usedOG={} # формируем используемые группы 
for line in fAclNewInside:
    if not ("remark" in line) and not ("icmp any4" in line):
         
        lLine=line.split()
        serv=lLine[5]
        usedServices[serv]=dObjectsGS[serv]
        if not ("any4 any4" in line):
            src=lLine[7]
            dst=lLine[9]
            
            
            if lLine[8]!="object":
                usedOG[src]=dObjectsGN[src]
                usedOG[dst]=dObjectsGN[dst]
            else:
                print ("А тут у нас объект!", lLine[8])


# оказывается нутри объектных групп могут быть другие групп. Соберём и их
usedOG2={}
for iKey in usedOG.keys():
    for iVal in usedOG[iKey]:
        if "group-object" in iVal:
            usedOG2[str(iVal).split()[1]]=dObjectsGN[str(iVal).split()[1]]


usedOGGeneral={**usedOG, **usedOG2}

#теперь надо понять что конфигурируем из используемых объектов
usedObjects={}

for iKey in usedOGGeneral.keys():
    for iVal in usedOGGeneral[iKey]:
        if (not "description" in iVal) and (not "group-object" in iVal) :
            if  iVal.split()[1]!="host":
                objName=iVal.split()[2]
            
                usedObjects[objName]=dObjects[objName]
            else:
                print ("Object with 'host' inside - ", iKey)



#### Запищем результат в файл

fAutConfig=open("objects_for_INSIDE_ACL.iso","w")
for i in usedObjects.keys():
    fAutConfig.write ("object network ")
    fAutConfig.write (i)
    fAutConfig.write ("\n")
    for j in usedObjects[i]:
        fAutConfig.write (j)
        fAutConfig.write ("\n")
fAutConfig.write ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
fAutConfig.write ("!!!!!!!!!!!!!!! Config groups !!!!!!!!!!!!!!!!!!\n")
fAutConfig.write ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
#Делаем конфигурацию для используемых групп
for i in usedOGGeneral.keys():
    fAutConfig.write ("object-group network ")
    fAutConfig.write (i)
    fAutConfig.write ("\n")
    for j in usedOGGeneral[i]:
        fAutConfig.write (j)
        fAutConfig.write ("\n")

fAutConfig.write ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
fAutConfig.write ("!!!!!!!!!!!!!!! Config services !!!!!!!!!!!!!!!!!!\n")
fAutConfig.write ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")           
#Делаем конфигурацию для используемых сервисов
for i in usedServices.keys():
    fAutConfig.write ("object-group service ")
    fAutConfig.write (i)
    fAutConfig.write ("\n")
    for j in usedServices[i]:
        fAutConfig.write (j)
        fAutConfig.write ("\n")

fAutConfig.close()
