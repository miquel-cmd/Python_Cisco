from typing import cast
from netmiko import ConnectHandler
import json
import csv
import time
from icmplib import *
import sys
import traceback

def csv_to_json(csvFilePath):
	jsonArray = []
      
    #read csv file
	with open(csvFilePath, encoding='utf-8') as csvf: 
		#load csv file data using csv library's dictionary reader
		csvReader = csv.DictReader(csvf) 

		#convert each csv row into python dict
		for row in csvReader: 
		    #add this python dict to json array
			jsonArray.append(row)
	return(jsonArray)


csvFilePath='input.csv'
array_json=csv_to_json(csvFilePath)

start_process=time.time()
f=open("RESULTADO.txt","w")
for i in array_json:

	dev1={
		#'device_type': 'cisco_ios',
		'device_type':i["type"],
  		'host': i["ip"],
		'username': i["username"],
		'password': i["password"],
		'secret':i["password"],
		'verbose':True
	}
	print(dev1)
	status=ping(i["ip"],count = 2)
	try:
		start_equipment=time.time()
		router_connection = ConnectHandler(**dev1)
		router_connection.enable()
		hostname = router_connection.send_command('show run | i hostname',expect_string='#')
		print('hostname: ',hostname)
		prompt=hostname.split(' ')[1].split('\n')[0].strip(" ")+'#'
		print('prompt:', prompt, 'hay salto')
		router_connection.send_command('term datadump', expect_string='#')
		showrun=router_connection.send_command('show running', expect_string=prompt)
		#showinv=router_connection.send_command('show inventory',expect_string=prompt)
		#showver=router_connection.send_command('show version',expect_string=prompt)
		router_connection.disconnect()
		file=prompt
		data= open(prompt+i["ip"]+'.txt',"w")
		#data.write("show running\n" + showrun +"\n\nshow inventory\n" + showinv + "\n\nshow version \n"+showver)
		data.write("show running\n" + showrun)
		data.close()
		f.write( i["ip"] + "," + "OK" +","+str(status.is_alive)+"\n")
		#print(f"Router {hostname} tarda:{time.time()-start_equipment}\n")
	except Exception as e:
		#print('errorrrrrrrrrrrrrrrrrrrrr' , str(e).split('\n')[0])
		f.write( i["ip"] + ","+str(e).split('\n')[0] +","+str(status.is_alive)+'\n')
		continue
print(f"El proceso ha tardardo un tiempo de: {time.time()-start_process}")
f.close()