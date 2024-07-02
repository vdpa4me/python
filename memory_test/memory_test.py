#telent connection
import getpass
import asyncio
import telnetlib3
import sys
import os
import time

target_time_min = 15
cmb = ""
ip = ""

async def main():

    #connect to a CMB
    print("connected to "+cmb+"("+ip+")")

    port = 23

    reader, writer = await telnetlib3.open_connection(ip, port, encoding='utf-8')
    print("connected")

    await reader.readuntil(b"login: ")
    writer.write("root".encode('ascii')+b"\n")
    await reader.readuntil(b"Password: ")
    writer.write("a".encode('ascii')+b"\n")
    print("Logged in")  

    #Memory Test
    print("1. start mtest (wait 1 minute)")
    writer.write("mkdir /root/log\n")
    writer.write("cd /root/log\n")
    writer.write("rm *\n")
    writer.write("cd /root/test\n")
    writer.write("./start_mtest.sh > /root/log/dimm_temp.log &\n")
    await asyncio.sleep(60)

    #CPU thermal recording
    #print("2. start ptst")
    #writer.write("cd /root/ptat\n")
    #writer.write("cd log\n")
    #writer.write("rm *\n")
    #writer.write("cd ..\n")
    #writer.write("./ptat -log -csv -wf -i 5000000 -t 0 &\n")
    #await asyncio.sleep(30)

    #wait 15 minutes
    print("3. wait "+ target_time_min+" minutes")
    time.sleep(60*target_time_min)

    #end test
    #print("4. end ptat")
    #writer.write("pkill -9 -f ptat\n")
    #await asyncio.sleep(30)

    print("5. end mtest")
    writer.write("cd /root/test\n")
    writer.write("pkill -9 -f start_mtest.sh\n")
    await asyncio.sleep(30)
    writer.write("./end_mtest.sh\n")
    await asyncio.sleep(30)

    print("6. set fan speed to 50% (wait 1 minute)")
    writer.write("/root/fan/fan_control.py --set_fans_pwm 50\n")
    await asyncio.sleep(60)

    print("7. logging")
    writer.write("### DIMMTEMP_START ###\n")
    writer.write("cat /root/log/dimm_temp.log\n")
    writer.write("### DIMMTEMP_END ###\n")
    #writer.write("### CPUTEMP_START ###\n")
    #writer.write("cat /root/ptat/log/*mon*\n")
    #writer.write("### CPUTEMP_END ###\n")
    await asyncio.sleep(30)

    dir_name = os.path.dirname(os.path.realpath(__file__))
    new_file_name = cmb + "_dimm_cpu.log"
    new_file_name = os.path.join(dir_name, new_file_name)
    newFile = open(new_file_name, 'w', encoding='utf8')
    newFile.write(reader.read_all().decode('utf8'))
  
    writer.close()
    reader.close()
    await writer.wait_closed()
    await reader.wait_closed()

    print("8. done")




if len(sys.argv) == 1:
    print("argument missing")
    sys.exit(1) 


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
elif sys.argv[1] == "13":
    cmb = "CMB13"
    ip = "198.168.0.1"
else:
    print("invalid argument")
    sys.exit(1)

asyncio.run(main())
