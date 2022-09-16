# Python_Ciscov0.1
get configuration from CSV

The input filename is by default input.csv and the results are saved into RESULTADOS.txt (both files must be in the same project folder).

The CSV input File must have the following header:

"ip,username,password,type"

The type is the connection option and could be one of the following options:

*Telnet: cisco_ios_telnet

*ssh: cisco_ios

Example:
If yoy want to review connectivity for 1.1.1.1 (telnet) and 2.2.2.2 (ssh) the input.csv file should be look like:

ip,username,password,type

1.1.1.1,username,password,cisco_ios

2.2.2.2,username1,password2,cisco_ios_telnet
