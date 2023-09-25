import sys
import os
import re
import pandas as pd

new_file_name = ''
print_list = []

#version 005

if __name__ == '__main__':

    # get current directory 
    dir_name = os.path.dirname(os.path.realpath(__file__))

    # get failes in the current directory 
    file_list = []
    file_name_for_tag = ""
    for (root, directories, files) in os.walk(dir_name):
        for file in files: 
            file_name_for_tag=file
            file_path = os.path.join(root, file)
            path,ext = os.path.splitext(file_path)
            if (ext in '.log') and "_LINUX_" not in file_path and "Run_" not in file_path:
                file_list.append(file_path)
    # list sort 
    file_list.sort()

    
    # new file for writing
    new_file_name = "CPULockupPorts.csv"
    new_file_name = os.path.join(dir_name, new_file_name)
    print("Output file:{}".format(new_file_name))


    # result_path = the current directory 
    result_path = dir_name

    
    print('START PARSING ... ')
    lockup_dut_list = []
    err_list = []
    lockup_dut_cnt = 0

    for file in file_list:
        interposer = ""
        dut_num = ""

        # initial read
        logfile = open(file, 'r', encoding='utf8', errors='ignore')
        current_line = logfile.readline()
        while current_line:
            # Skip empty line
            if current_line == '\n':
                current_line = logfile.readline()
                continue
            elif "], Interposer   :" in current_line:
                #A,23/07/26,10:10:56:867603,[1], Interposer   : ANSKR22446158607500
                tokens = current_line.split(',')
                dut_num = tokens[3].replace('\n','')
                tmp_str = tokens[4]
                sub_tokens = tmp_str.split(':')
                interposer = sub_tokens[1]
                interposer = interposer.strip()
                interposer = interposer.replace("\n","")
            elif "],Link change:" in current_line:
                #A,23/07/26,10:11:21:693531,[1],Link change:  Up 8.0G 4L Train LAB LTSSM=8.2 (raw reg=82000479 c/s=98430040)
                if dut_num in current_line:
                    EndTraing = False
                    continue_cnt = 0
                    while(EndTraing == False):
                        current_line = logfile.readline()
                        if (dut_num in current_line) and ("],Link change:" in current_line):
                            continue_cnt = continue_cnt + 1
                        else:
                            EndTraing = True
                    
                    if continue_cnt > 100 :
                        dut = interposer + "," + dut_num + ","+str(continue_cnt)
                        lockup_dut_cnt = lockup_dut_cnt + 1
                        lockup_dut_list.append(dut)
            elif ",ERROR:" in current_line and (dut_num in current_line):
                tmp = current_line.replace("\n","")
                err_msg = interposer + "," + dut_num + ","+tmp
                err_list.append(err_msg)
            current_line = logfile.readline()
        logfile.close()

    # write a file 
    newFile = open(new_file_name, 'w', encoding='cp949')
    newFile.write("Total CPU lock up port : {}\n".format(lockup_dut_cnt))
    cnt = 0
    for dut in lockup_dut_list:
        cnt = cnt + 1
        newFile.write("{}, {}\n".format(cnt,dut))
    cnt = 0
    for err in err_list:
        cnt = cnt + 1
        newFile.write("{}, {}\n".format(cnt,err))
    
    newFile.close()