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

#Memory Test 
print("1. start mtest (wait 1 minute)")
tn.write(b"mkdir /root/log\n")    
tn.write(b"cd /root/log\n") 
tn.write(b"rm *\n")
tn.write(b"cd /root/test\n")
tn.write(b"./start_mtest.sh > /root/log/dimm_temp.log &\n")
time.sleep(60)

#CPU thermal recording 
print("2. start ptst")
tn.write(b"cd /root/ptat\n")
tn.write(b"cd log\n")
tn.write(b"rm *\n")
tn.write(b"cd ..\n")
tn.write(b"./ptat -log -csv -wf -i 5000000 -t 0 &\n")
time.sleep(30)

print("3. wait 15 minutes")
time.sleep(60*15)
print("4. end ptat")
tn.write(b"pkill -9 -f ptat\n")      
print("5. end mtest")
time.sleep(30)
tn.write(b"cd /root/test\n")
tn.write(b"pkill -9 -f start_mtest.sh\n")
time.sleep(30)
tn.write(b"./end_mtest.sh\n")
print("6. set fan speed to 50% (wait 1 minute)")
tn.write(b"/root/fan/fan_control.py --set_fans_pwm 50\n")
time.sleep(60)


print("7. logging")
tn.write(b"### DIMMTEMP_START ###\n")
tn.write(b"cat /root/log/dimm_temp.log\n")
tn.write(b"### DIMMTEMP_END ###\n")
tn.write(b"### CPUTEMP_START ###\n")
tn.write(b"cat /root/ptat/log/*mon*\n")  
tn.write(b"### CPUTEMP_END ###\n")

tn.write(b"exit\n")

dir_name = os.path.dirname(os.path.realpath(__file__))
new_file_name = cmb + "_dimm_cpu.log"
new_file_name = os.path.join(dir_name, new_file_name)
newFile = open(new_file_name, 'w', encoding='utf8')
newFile.write(tn.read_all().decode('utf8'))

print("8. done")
