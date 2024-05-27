import sys
import os
import re
from os.path import basename

report_list = []

if __name__ == '__main__':

    # get current directory 
    dir_name = os.path.dirname(os.path.realpath(__file__))

    # get failes in the current directory 
    file_list = []
    for (root, directories, files) in os.walk(dir_name):
        for file in files:
            file_path = os.path.join(root, file)
            path,ext = os.path.splitext(file_path)
            if ext in '.rep' :
                temp_dic = {}
                # new file for writing
                temp_dic['read'] = file_path
                file_list.append(temp_dic)

    for file_dic in file_list:
        read_file = file_dic['read']

        # dictionary for storing the data
        port_info_dic = {}
        
        # initial read
        logfile = open(read_file, 'r', encoding='utf8', errors='ignore')
        current_line = logfile.readline()    
        while current_line:
            # Skip empty line
            
            if "NEOSEM TEST REPORT FOR RACK" in current_line:
                #NEOSEM TEST REPORT FOR RACK  00 Port 113 Device 00
                result = re.findall(r'\d+', current_line)
                port = result[1]
                port_info_dic['port'] = port
            elif "User MN     S/N" in current_line:
                current_line = logfile.readline() # read one more line
                tokens = current_line.split(' ')

                #dump tokens
                #for i in range(0,len(tokens)):
                #    print("["+str(i)+"]"+tokens[i])
                #exit(1)
                port_info_dic['sn'] = tokens[2]
                tmp = tokens[18]
                tmp = tmp.replace('\n','')  
                port_info_dic['duration'] = tmp
            current_line = logfile.readline()
        logfile.close()
        report_list.append(port_info_dic)


    # wirte to report
    with open("Total.csv", 'w') as rf:
        rf.write("##############################################\n")
        rf.write("Total \n")
        rf.write("##############################################\n")
        rf.write("\n")
        rf.write("No, Port, SSD S/N, Duration\n")
        report_list.sort(key=lambda x: x['port'], reverse=False)
        cnt = 1
        for i in range(0, len(report_list)):
            port_info_dic = report_list[i]
            rf.write( str(cnt)+","+  str(port_info_dic['port'])+","+  str(port_info_dic['sn'])+","+ str(port_info_dic['duration'])+"\n")
            cnt = cnt + 1
        rf.write("\n")
        rf.close()
    


