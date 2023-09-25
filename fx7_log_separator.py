import sys
import os
from os.path import basename
import re

new_file_name = ''
print_list = []

new_file_names = []

PIN_STATE_IDLE = 0
PIN_STATE_PERST_ASSERT = 1
PIN_STATE_PWDIS_ASSERT = 2


if __name__ == '__main__':

    # get current directory 
    dir_name = os.path.dirname(os.path.realpath(__file__))

    # get failes in the current directory 
    file_list = []
    for (root, directories, files) in os.walk(dir_name):
        for file in files:
            file_path = os.path.join(root, file)
            path,ext = os.path.splitext(file_path)
            if ext in '.log' :
                file_list.append(file_path)
    # list sort 
    file_list.sort()

    # new file for writing
    new_file_name = "fx7_test_summary.csv"
    new_file_name = os.path.join(dir_name, new_file_name)

    # result_path = the current directory 
    result_path = dir_name

    print('Checking Number of DUTs  ... ')
    cnt=0

    for file in file_list:

        # initial read
        logfile = open(file, 'r', encoding='utf8', errors='ignore')
        current_line = logfile.readline()
        dut_list = []
        while current_line:
            # Skip empty line
            if current_line == '\n':
                current_line = logfile.readline()
                continue
            elif "libfx6nvme.a Version =" in current_line:
                #[2023-03-10 10:11:28:274][ANSKR23036158605300-1-1] libfx6nvme.a Version = 7.5, Jan 31 2023 14:19:28 SiteMask=ffff
                tokens = current_line.split(']')
                dut_num = tokens[1].replace('[','')
                dut_num = dut_num + "]"
                dut_list.append(dut_num)
            elif "HARDWARE SORT BIN" in current_line:
                break;
            current_line = logfile.readline()
        logfile.close()

        #remove redundancy
        dut_set = set(dut_list)
        dut_list = list(dut_set)
        dut_list.sort()
        total_cnt = 0
        fail_cnt = 0
        for dut in dut_list:
            dut_position = str(dut)

            logfile = open(file, 'r', encoding='utf8', errors='ignore')
            fpath, fname = os.path.split(logfile.name)
            write_file = fname.rstrip('.log') + "_"+ dut_position + ".log"
            write_file = os.path.join(dir_name, write_file)
            writeLogFile = open(write_file, 'w', encoding='utf8', errors='ignore')

            current_line = logfile.readline()
            isTestEnd = False;
            isTestPass = False;
            failCate = "";
            print(dut_position)
            while current_line:
                if dut_position in current_line:
                    writeLogFile.write(current_line)
                    if "################# HandlerSort ################" in current_line:
                        isTestEnd = True
                    elif "FATAL ERROR" in current_line:
                        isTestEnd = True
                        isTestPass = False
                        if "SetPCIeRST(eFunctional)" in current_line :
                            failCate = "SetPCIeRST_TO"
                    elif "] HARDWARE SORT BIN = 1" in current_line:
                        isTestPass = True
                    elif "] ERROR VDDQ(V):" in current_line:
                        failCate = "ERRORVDDQ"
                    elif "ERROR: my pcie address is unfound" in current_line:
                        failCate = "NO_PCIE_FOUND"
                    elif "ERROR PCIe Link" in current_line:
                        failCate = "PCIE_LINK"

                        
                current_line = logfile.readline()
            writeLogFile.close()
            logfile.close()

            #if isTestEnd == True and isTestPass == True:
            #    os.rename(write_file,write_file+".testDone_Pass.log")
            if isTestEnd == True and isTestPass == False:
                os.rename(write_file,write_file+".testDone_Fail_"+failCate+".log")
