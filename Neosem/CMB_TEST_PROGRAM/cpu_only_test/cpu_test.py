#telent connection
import getpass
import asyncio
import telnetlib
import sys
import os
import time

if len(sys.argv) == 1:
    print("argument missing")
    sys.exit(1) 


cmb = ""
ip = ""
if sys.argv[1] == "1":
    cmb = "CMB1"
    ip = "192.168.0.1"
elif sys.argv[1] == "2":
    cmb = "CMB2"
    ip = "192.168.0.2"
elif sys.argv[1] == "3":
    cmb = "CMB3"
    ip = "192.168.0.3"
elif sys.argv[1] == "4":
    cmb = "CMB4"
    ip = "192.168.0.4"
elif sys.argv[1] == "5":
    cmb = "CMB5"
    ip = "192.168.0.5"
elif sys.argv[1] == "6":
    cmb = "CMB6"
    ip = "192.168.0.6"
elif sys.argv[1] == "7":
    cmb = "CMB7"
    ip = "192.168.0.7"
elif sys.argv[1] == "8":
    cmb = "CMB8"
    ip = "192.168.0.8"
elif sys.argv[1] == "9":
    cmb = "CMB9"
    ip = "192.168.0.9"
elif sys.argv[1] == "10":
    cmb = "CMB10"
    ip = "192.168.0.10"
elif sys.argv[1] == "11":
    cmb = "CMB11"
    ip = "192.168.0.11"
elif sys.argv[1] == "12":
    cmb = "CMB12"
    ip = "192.168.0.12"
else:
    print("invalid argument")
    sys.exit(1)

#connect to a CMB
print("connected to "+cmb+"("+ip+")")
tn = telnetlib.Telnet(ip)
tn.read_until(b"login: ")
tn.write("root".encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write("a".encode('ascii') + b"\n")

#ptat 
print("1. start ptat test (wait 1 minute)")
tn.write(b"mkdir /root/log\n")    
tn.write(b"cd /root/log\n") 
tn.write(b"rm *\n")

tn.write(b"cd /root/ptat\n")
tn.write(b"cd log\n")
tn.write(b"rm *\n")
tn.write(b"cd ..\n")
time.sleep(10)
tn.write(b"./ptat -ct 1 -mon > /root/log/cput_temp.log &\n")
time.sleep(10)

print("2. wait 1 minutes")
time.sleep(60*1)
print("3. end ptat")
tn.write(b"pkill -9 -f ptat\n")
time.sleep(10)

print("4. logging")
tn.write(b"### CPU_LOG_START ###\n")
tn.write(b"cat /root/log/cput_temp.log\n")
tn.write(b"### CPU_LOG_END ###\n")
tn.write(b"exit\n")

dir_name = os.path.dirname(os.path.realpath(__file__))
new_file_name = cmb + "_cpu.log"
new_file_name = os.path.join(dir_name, new_file_name)
newFile = open(new_file_name, 'w', encoding='utf8')
newFile.write(tn.read_all().decode('utf8'))

print("5. done")
