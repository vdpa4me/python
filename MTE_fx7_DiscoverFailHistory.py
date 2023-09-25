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
    new_file_name = "DiscoverFailHistory.csv"
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
        discover_done_cnt = 1
        fail_cate =""
        while current_line:
            # Skip empty line
            if current_line == '\n':
                current_line = logfile.readline()
                continue
            elif "], Interposer   :" in current_line: #starting point
                #A,23/07/26,10:10:56:867603,[1], Interposer   : ANSKR22446158607500
                tokens = current_line.split(',')
                dut_num = tokens[3].replace('\n','')
                tmp_str = tokens[4]
                sub_tokens = tmp_str.split(':')
                interposer = sub_tokens[1]
                interposer = interposer.strip()
                interposer = interposer.replace("\n","")
                discover_done_cnt = 1 #init
            elif (",TB PCIeDiscover execution time" in current_line) and (dut_num in current_line) and ("0.000 seconds" not in current_line):
                discover_done_cnt = discover_done_cnt + 1
            elif (",Recipe Result " in current_line) and (dut_num in current_line) and ("Bin 255 (0xff)" not in current_line):
                tmp = current_line.replace("\n","")
                err_msg = interposer + "_" + dut_num + ","+str(discover_done_cnt)
                err_list.append(err_msg)
                WasFound=True
            current_line = logfile.readline()
        logfile.close()

    # write a file 
    newFile = open(new_file_name, 'w', encoding='cp949')
    cnt = 0
    newFile.write("No,Interposer_DUT#,loop Cnt at fail\n")
    for dut in err_list:
        cnt = cnt + 1
        newFile.write("{}, {}\n".format(cnt,dut))

    
    newFile.close()