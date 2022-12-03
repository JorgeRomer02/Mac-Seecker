#PARA PODER VER EL CODIGO DE MEJOR FORMA, SE RECOMIENDA LA EXTENCION "Better Comments" EN VISUAL STUDIO CODE
#by KH
#IMPORTACIONES ----------------------------------------------------------# (Importacion de las librerias a usar)
from netmiko import *
from netmiko import ConnectHandler
from time import *
import re
import json
import os

#BIENVENIDA  -------------------------------------------------------------#
os.system('cls')
print("---------------------------------------------------------------------------------------------------------")
print('''
`7MMM.     ,MMF'                      .M"""bgd                            `7MM                        
  MMMb    dPMM                       ,MI    "Y                              MM                        
  M YM   ,M MM   ,6"Yb.   ,p6"bo     `MMb.      .gP"Ya   .gP"Ya   ,p6"bo    MM  ,MP' .gP"Ya  `7Mb,od8 
  M  Mb  M' MM  8)   MM  6M'  OO       `YMMNq. ,M'   Yb ,M'   Yb 6M'  OO    MM ;Y   ,M'   Yb   MM' "' 
  M  YM.P'  MM   ,pm9MM  8M       mm .     `MM 8M"""""" 8M"""""" 8M         MM;Mm   8M""""""   MM     
  M  `YM'   MM  8M   MM  YM.    ,    Mb     dM YM.    , YM.    , YM.    ,   MM `Mb. YM.    ,   MM     
.JML. `'  .JMML.`Moo9^Yo. YMbmd'     P"Ybmmd"   `Mbmmd'  `Mbmmd'  YMbmd'  .JMML. YA. `Mbmmd' .JMML.   
''')

print("---------------------------------------------------------------------------------------------------------")
print("Proyecto: Bucador de MAC en topologia | Jorge Alejandro Romero Vazquez | 4A".center(95))
print("---------------------------------------------------------------------------------------------------------\n")

#MAC OBJETIVO Y FORMATEO --------------------------------------------------# (Obtencion de la mac y formateo auno que me sirva mas)
'''
Variables:
- target:                                       Mac a buscar
- switch:                                       Ip o domainname del switch a conectar
- user:                                         Usuario  ssh del switch
- u_pass:                                       Password ssh del swith
- e_pass:                                       Password del modo privilegiado
- device:                                       diccionario para almacenar las credenciales ssh
- connect_device:                               conexion con el switch
'''

#INGRESA MAC OBJETIVO ----------------------------|
target = input("Mac objetivo:\n>> ")
target = target.replace("-","")
target = target.lower()
traget = ("by KH")

#CONEXION CON SWITCH 1 ---------------------------------------------------# (Conexion con el primer switch por ssh, para empezar)

#by KH
#CREDENCIALES SSH PARA EL PRIMER SWITCH ------------|
switch = input("\nIP primer switch:\n>> ")
user = input("\nUsuario:\n>> ")
u_pass = input("\nContraseña:\n>> ")
e_pass = "cisco"

#CONECION CON EL SWITCH---------------------------|
device = {
    "host":switch,
    "username":user,
    "password":u_pass,
    "device_type":"cisco_ios",
    "secret": e_pass,}

try:
    connect_device = ConnectHandler(**device)
    connect_device.enable()

except:
    print("Revise las credenciales ssh y vuelva a intentar")
    ciclo=0

ciclo = 1
while ciclo == 1:
    #BUSQUEDA DE VECINOS CDP-----------------------------------------------#kh(busqueda de los vecionos cdp y almacenamiento de datos de cada vecino)
    try:#//try CDP
        '''
        Variables:
        - output_cdp:                           Salida del comando
        - cdp_json:                             Salida del comando en formato json
        - sw_n:                                 Cantidad de vecinos
        - cdp_lst:                              Lista de ip, nombre y puerto de cada vecino
        - sw:                                   Swich x
        - cdp_name:                             Nombre del switch x
        - cdp_ip:                               Ip del switch x
        - cdp_port:                             Puerto del switch x
        - port_f:                               Formateo de la respuesta del puerto
        - ciclo:                                control del while para poder terminarlo abruptamente
        - by KH
        '''

        #RESULTADO CDP---------------------------------|
        output_cdp = connect_device.send_command("show cdp neighbors detail",use_textfsm = True)#//recibe respuesta del comando en variable
        output_cdp = (json.dumps(output_cdp, indent = 2))#//Se reduce la cantidad de datos
        cdp_json = json.loads(output_cdp)#//Se transorma el texto plano en un formato json

        sw_n = (len(cdp_json))#//cantidad de vecinos en el Json
        cdp_lst = []
        #by KH

        #ALMACENAMIENTO DE DATOS DE LOS VECINOS-----------|
        print("\n---------------------------------------------------------------------------------------------------------\n")
        print("TABLA CDP:".center(60))
        print("-------------------------------------------------------------")
        print(("    |"),("Nombre").center(20),"|",("IP_CDP").center(15),"|",("Puerto").center(14),"|")
        print("-------------------------------------------------------------")

        if sw_n==0:#//Si no hay vecinos, la tabla cdp se imprime sola
            print("Sin Vecinos".rjust(35))
            cdp_lst.append({"destination_host":"-  -  -","management_ip":"-  -  -","local_port":"-  -  -"})

        for sw  in range(sw_n):#//Almacena los datos utiles de los vecinos
            cdp_name = (cdp_json[sw]["destination_host"])
            cdp_ip = (cdp_json [sw]["management_ip"])
            cdp_port = (cdp_json[sw]["local_port"])

            #FORMATEO PUERTO-----------------------------|
            try:#//formatea resultado del puerto para el formato (Fa x/x/x)
                port_f=list(cdp_port)
                cdp_port=""
                dellist=("s","t","E","t","h","e","r","n","e","t")
                
                for letra in dellist:#//Elimina letras que no sirven
                    port_f.remove(letra)

                for letter in port_f:#//Almacena letras restantes en cadena
                    cdp_port+=letter

                cdp_port=str(cdp_port)#//Almacena dato e imprime

            #FORMATEO PUERTO-----------------------------|
            except:#//formatea resultado del puerto para el formato (Gi x/x/x)
                port_f = list(cdp_port)
                cdp_port = ""
                dellist = ("i","g","a","b","i","t","E","t","h","e","r","n","e","t")

                for letra in dellist:#//Elimina letras que no sirven
                    port_f.remove(letra)

                for letter in port_f:#//Almacena letras restantes en cadena
                    cdp_port+=letter

                cdp_port = str(cdp_port)#//Almacena dato e imprime

            #IMPRESION DE TABLA CDP ---------------------|
            print(f"{sw:>2}  | {cdp_name:^20} | {cdp_ip:^15} | {cdp_port:^15}|")#//Tabla de vecinos
            print("-------------------------------------------------------------")

            #ALMACENAMIENTO DE VECINOS-------------------|
            cdp_lst.append({"destination_host":cdp_name,"management_ip":cdp_ip,"local_port":cdp_port})
    #by KH
    except:#//try_CDP
        print("Error en la busqueda de CDP neighbors")
        break

    #BUSQUEDA DE MAC-----------------------------------------------------#(Busqueda de conicidencias de mac en los puertos del switch)
    try:#//try_MAC
        '''
        Variables:
        - output_mac:                           Salida del comando
        - mac_json:                             Salida del comando en formato json
        - mac_n:                                Cantidad de mac en la tabla
        - mac_lst:                              Lista de ip y puerto de cada mac en la respuesta
        - mac:                                  Cantidad de Macs
        - mac_ip:                               Ip de mac x
        - mac_port:                             Puerto de mac x
        - mac_s:                                Mac actual en el ciclo
        - mac_q:                                Formato de mac que se busca
        - mac_r:                                Respuesta Mac que coincide
        - mac_f:                                Formateo de la mac respuesta
        '''

        #COMANDO MACC ADDRESS-TABLE-------------------|
        output_mac = connect_device.send_command("show mac address-table",use_textfsm = True)#//recibe respuesta del comando en variable

        output_mac = (json.dumps(output_mac, indent = 2))#//Se reduce la cantidad de datos
        mac_json = json.loads(output_mac)#//Se transorma el texto plano en un formato json

        mac_n = (len(mac_json))#//cantidad de MACs en el Json
        mac_lst = []

        #ALMACENAMIENTO DE MAC------------------------|
        for mac in range(mac_n) :#//Almacena los datos necesarios de cada mac

            mac_ip = (mac_json[mac]["destination_address"])
            mac_port = (mac_json[mac]['destination_port'])

            mac_lst.append({'destination_address':mac_ip , 'destination_port': mac_port})

            #FORMATEO DE MAC QUERY-----------------------|
            mac_s = (mac_lst[mac]['destination_address'])#//MAC Source
            mac_q = re.compile(r"\w\w\w\w.\w\w\w\w.\w\w\w\w")#//MAC query
            mac_r = (mac_q.search(mac_s))#//MAC re

            Mac_f = mac_r.group()#//MAC Formated
            Mac_f = Mac_f.replace(".","")#//MAC Formated
            Mac_f = Mac_f.lower()#//MAC Formated

            #SE REMPLAZA EL DATO EXISTENTE CON EL FORMATEADO
            mac_json[mac]["destination_address"] = Mac_f

    except:#//try_MAC
        print("Error en la busqueda de MACs dentro de las interfaces del switch")
        break
   
    #print("MAC correcto")
    
    #CONEXION CON EL SIGUIENTE SWITCH----------------------------------------#(Conexion con la ip que conicide con puerto y mac de la busqueda)

    #try:#//try_CON
    '''
    Variables:
    - mac:                                      Cantidad de Macs                                                  
    - mac_n:                                    Cantidad de mac en la tabla                                           
    - target:                                   Mac objetivo de busqueda
    - mac_json:                                 Salida del comando en formato json
    - puerto:                                   Puerto asignado a la mac que coincide
    - puerto_t:                                 Obtiene el puerto del vecino que coincide con esta  
    '''
#by KH
    for mac in range(mac_n):#//Se busca por cada mac en la lista

    #COMPARA CADA MAC CON LA MAC TARGET ------------|
        if target == (mac_json[mac]['destination_address']):

            rmac = (mac_json[mac]['destination_address'])
            #OBTIENE EL PUERTO DE LA MAC TARGET -----------|
            puerto = (mac_json[mac]['destination_port'])[0]
        
        else:
            #Si no sesta la mac en ese puesto, se va al siguiente
            pass

    for sw in range(sw_n):#//Por cada switch vecino

        puerto_t = (cdp_lst[sw]["local_port"])#//Obtiene los datos necesarios
        ip_ssh = (cdp_lst[sw]["management_ip"])
    
        if puerto == puerto_t:#//Compara el peurto de la mac, con los puertos vecinos 

            #CREDENCIALES SSH PARA EL PRIMER SWITCH ------------|
            print("\n---------------------------------------------------------------------------------------------------------")
            print(f"Conexion con ip {ip_ssh}\n")
            
            #CONECION CON EL SWITCH---------------------------|
            device = {
                "host": ip_ssh,
                "username": user,
                "password": u_pass,
                "device_type": "cisco_ios",
                "secret": e_pass,}
            
            connect_device = ConnectHandler(**device)
            connect_device.enable()

        else:#//Si no hubo coincidencia con los puertos significa que es el host target
            
            output_run = connect_device.send_command("show run | include hostname",use_textfsm = True)#//comando show run, para obtener el nombre del switch             
            #SE IMPRIMEN RESUTADOS DE LA BUSUQUEDA------------------|              
            print("\n---------------------------------------------------------------------------------------------------------")
            print("MAC ENCONTRADA:".center(60))
            print(f"\nMac {target.upper()} encontrada en")
            print(f"Conectado al puerto {puerto} en {output_run}")
            print("---------------------------------------------------------------------------------------------------------")
            ciclo=0
            break

    #except:
        print("Error de conexion/mac")
        break

#by KH
