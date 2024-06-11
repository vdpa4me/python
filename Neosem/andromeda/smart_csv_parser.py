import sys
import os
import re
from os.path import basename

report_list = []
smart_list = []

if __name__ == '__main__':

    # get current directory 
    dir_name = os.path.dirname(os.path.realpath(__file__))

    # get failes in the current directory 
    file_list = []
    for (root, directories, files) in os.walk(dir_name):
        for file in files:
            file_path = os.path.join(root, file)
            path,ext = os.path.splitext(file_path)
            if ext in '.csv' :
                temp_dic = {}
                # new file for writing
                temp_dic['read'] = file_path
                file_name = basename(file_path)
                file_name = file_name.replace('.csv','')
                temp_dic['read_file_only'] = file_name
                file_list.append(temp_dic)

    
    for file_dic in file_list:
        read_file = file_dic['read']
        read_file_only = file_dic['read_file_only']

        # dictionary for storing the data
        dut_info_dic = {}
        dut_info_dic['1sn'] = read_file_only

        # initial read
        logfile = open(read_file, 'r', encoding='utf8', errors='ignore')
        current_line = logfile.readline()    
        
        while current_line:
            # Skip empty line
            if "Byte 0" in current_line:
                tokens = current_line.split(',')
                key = tokens[1].replace(' ','')
                value = tokens[2].replace(' ','')
                value = value.replace('\n','')
                dut_info_dic[key] = value
            current_line = logfile.readline()
        logfile.close()

        smart_list.append(dut_info_dic)

    # to rep parsing
    rfile_list = []
    for (root, directories, files) in os.walk(dir_name):
        for file in files:
            file_path = os.path.join(root, file)
            path,ext = os.path.splitext(file_path)
            if ext in '.rep' :
                temp_dic = {}
                # new file for writing
                temp_dic['read'] = file_path
                rfile_list.append(temp_dic)
    
    for file_dic in rfile_list:
        read_file = file_dic['read']

        # dictionary for storing the data
        port_info_dic = {}
        
        # initial read
        logfile = open(read_file, 'r', encoding='utf8', errors='ignore')
        current_line = logfile.readline()    
        
        isSkip = False
        isASPMFailed = False

        while current_line:
            # Skip empty line
            if "Device Not selected" in current_line:
                isSkip = True
                break
            elif "Improperly defined variable;" in current_line:
                isASPMFailed = True
            elif "NEOSEM TEST REPORT FOR RACK" in current_line:
                #NEOSEM TEST REPORT FOR RACK  00 Port 113 Device 00
                result = re.findall(r'\d+', current_line)
                port = result[1]
                print("port:"+port)
                port_info_dic['port'] = port
            elif "ANDROMEDA TEST REPORT FOR RACK" in current_line:
                #ANDROMEDA TEST REPORT FOR RACK  00 Port 07 Device 00
                result = re.findall(r'\d+', current_line)
                port = result[1]
                print("port:"+port)
                port_info_dic['port'] = port
            elif "Model #:" in current_line:
                tokens = current_line.split(':')
                model = tokens[1].replace('\n','')
                model = model.replace(' ','')
                port_info_dic['model'] = model
                print("model:"+model)
            #Rev Level:     1107AXLA         Capacity:     000000001DCF32B0
            elif "Rev Level:" in current_line:
                tokens = current_line.split(' ')
                rev = tokens[6]
                port_info_dic['rev'] = rev
                print("rev:"+rev)
            elif "User MN     S/N" in current_line:
                current_line = logfile.readline() # read one more line
                tokens = current_line.split(' ')
                port_info_dic['sn'] = tokens[2]
                tmp = tokens[18]
                tmp = tmp.replace('\n','')  
                port_info_dic['duration'] = tmp

                for i in range(0,len(smart_list)):
                    dut_info_dic = smart_list[i]
                    sn1 = dut_info_dic['1sn']
                    sn1 = sn1.replace(' ','')   
                    sn2 = port_info_dic['sn']
                    sn2 = sn2.replace(' ','')
                    if sn1 == sn2:
                        port_info_dic['smart'] = dut_info_dic
                        print("S/N matching : "+sn1)
                        break
            current_line = logfile.readline()
        logfile.close()
    
        if isASPMFailed == True:
            port_info_dic['aspm'] = "Failed"
        else:
            port_info_dic['aspm'] = "Passed"

        if isSkip == False:
            print("[PORT_DIC_APPEND]")
            report_list.append(port_info_dic)

        
    # wirte to report
    with open("SmartRepTotal.csv", 'w') as rf:
        
        report_list.sort(key=lambda x: x['port'], reverse=False)

        header = "no,Port, Model, FW Rev, SSD S/N, Duration, ASPM fail"
        header_dut_info_dic = smart_list[0]
        for key in header_dut_info_dic.keys():
            header = header + "," + key 
        header = header + "\n"
        print(header)   
        rf.write(header)

        report_list.sort(key=lambda x: x['port'], reverse=False)
        cnt = 1
        for i in range(0, len(report_list)):
            port_info_dic = report_list[i]
            body = str(cnt)+","+ str(port_info_dic['port'])+","+ str(port_info_dic['model'])+","+str(port_info_dic['rev'])+","+  str(port_info_dic['sn'])+","+ str(port_info_dic['duration'])+","+port_info_dic['aspm']
            dut_info_dic = port_info_dic['smart']
            for key in dut_info_dic.keys():
                body = body + ","+dut_info_dic[key]
            body = body + "\n"
            print(body)
            rf.write(body)
            cnt = cnt + 1
        rf.write("\n")
        rf.close()
    


