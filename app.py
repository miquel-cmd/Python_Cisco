from typing import cast
from netmiko import ConnectHandler
import json
import csv
import time
from icmplib import *

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


csvFilePath='data.csv'
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
		'verbose':True
	}
	print(dev1)
	status=ping(i["ip"],count = 2,interval=0.2)
	try:
		start_equipment=time.time()
		router_connection = ConnectHandler(**dev1)
		router_connection.enable()
		hostname = router_connection.send_command('show run | i hostname',expect_string='#')
		print('hostname: ',hostname)
		prompt=hostname.split(' ')[1].split('\n')[0].strip(" ")+'#'
		print('prompt:', prompt, 'hay salto')
		#router_connection.send_command('term datadump', expect_string='#')
		#showrun=router_connection.send_command('show running', expect_string=prompt)
		#showinv=router_connection.send_command('show inventory',expect_string=prompt)
		#showver=router_connection.send_command('show version',expect_string=prompt)
		router_connection.disconnect()
		file=prompt
		#f= open(prompt+i["ip"]+'.txt',"w")
		#f.write("show running\n" + showrun +"\n\nshow inventory\n" + showinv + "\n\nshow version \n"+showver)
		#f.close()
		f.write( i["ip"] + "," + prompt +","+str(ping.is_alive)+"\n")
		print(f"Router {hostname} tarda:{time.time()-start_equipment}\n")
	except Exception as e:
		#print('error', str(e))
		f.write( i["ip"] + ","+str(e) +",",str(ping.is_alive)+'\n')
  		#router_connection.disconnect()
		continue
print(f"El proceso ha tardardo un tiempo de: {time.time()-start_process}")
f.close()