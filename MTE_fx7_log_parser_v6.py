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
            if (ext in '.log')and ("Run_" in file_path):
                file_list.append(file_path)
    # list sort 
    file_list.sort()

    
    # new file for writing
    new_file_name = file_name_for_tag + ".ouput.csv"
    new_file_name = os.path.join(dir_name, new_file_name)
    print("Output file:{}".format(new_file_name))


    # new file for writing
    #new_file_name = "fx7_test_summary.csv"
    #new_file_name = os.path.join(dir_name, new_file_name)

    murge_file = "RunLogMurged.log"
    murge_file = os.path.join(dir_name, murge_file)


    # result_path = the current directory 
    result_path = dir_name

    
    cnt=0
    
    RunID = ""
    Recipe = ""
    exe= ""
    
    pass_cnt = 0
    fail_cnt = 0
    test_cnt = 0
    if len(file_list) > 1 :
        # file murge
        file_list.sort()
        
        cmd = 'cmd /c type '
        for file in file_list:
            print(file)
            cmd = cmd + file +" "
            #with open(file, 'r',encoding='utf8') as infile:
            #    outfile.write(pd.read_csv(infile))
            #outfile.write("\n")
        cmd = cmd + " > " + murge_file
        print(cmd)

        print('START MERGING ... ')
        os.system(cmd)
        #sys.exit(0)
        
        file_list.clear()
        file_list.append(murge_file)
    
    print('START PARSING ... ')
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
            elif "] Starting Run: RunId:" in current_line:
                #[2023-06-27 17:34:10:202] Starting Run: RunId: 1687862049
                tokens = current_line.split(':')
                RunID = tokens[5].replace('\n','')
            elif "] Recipe File:" in current_line:
                #[2023-06-27 17:34:10:202] Recipe File:  C:\Tanisys\DNA2\User\mpdata\Auriga_FX7_Echo_MAIN_8TB_V0.84.xml
                tokens = current_line.split(':')
                Recipe = tokens[5].replace('\n','')
            elif "] Recipe EXE:" in current_line:
                #[2023-06-27 17:34:10:202] Recipe EXE: C:\Tanisys\DNA2\User\mpdata\FADU_FX7_Echo_MP_V0.89N.exe
                tokens = current_line.split(':')
                exe = tokens[5].replace('\n','')
            elif "libfx6nvme.a Version =" in current_line:
                #[2023-03-10 10:11:28:274][ANSKR23036158605300-1-1] libfx6nvme.a Version = 7.5, Jan 31 2023 14:19:28 SiteMask=ffff
                tokens = current_line.split(']')
                dut_num = tokens[1].replace('[','')
                dut_num = dut_num + ']'
                print(dut_num)
                dut_list.append(dut_num)
            current_line = logfile.readline()
        logfile.close()

        print('# of DUT : {}'.format(len(dut_list)))

        for dut in dut_list:
            dut_position = str(dut)

            logfile = open(file, 'r', encoding='utf8', errors='ignore')
            fpath, fname = os.path.split(logfile.name)

            test_cnt = test_cnt + 1

            #print(dut_position)

            cnt=cnt+1
            print_item_dic = {}
            print_item_dic['NO'] = cnt
            print_item_dic['DUT'] = dut_position
            print_item_dic['START_TIME'] = ""
            print_item_dic['LIB'] = ""
            print_item_dic['BLADE'] = ""
            print_item_dic['PB'] = ""
            print_item_dic['DPS'] = ""
            print_item_dic['INTERPOSER'] = ""
            print_item_dic['TBSIGNAL'] = ""
            print_item_dic['TBPOWER'] = ""
            print_item_dic['TEST_BLOCK'] = ""
            print_item_dic['FAIL_MSG'] = ""
            print_item_dic['RESULT'] = ""

            cur_test_block = ""
            cur_test_block = ""
            
            current_line = logfile.readline()
            while current_line:
                # Skip empty line
                if current_line == '\n':
                    current_line = logfile.readline()
                    continue
                elif ("libfx6nvme.a Version =" in current_line) and (dut_position in current_line):
                    #[2023-03-10 10:11:28:274][ANSKR23036158605300-1-1] libfx6nvme.a Version = 7.5, Jan 31 2023 14:19:28 SiteMask=ffff
                    tokens = current_line.split(']')
                    start_time = tokens[0].replace('[','')
                    library = tokens[2].replace('\n','')
                    library = library.replace(',','|')
                    print_item_dic['START_TIME']=start_time
                    print_item_dic['LIB'] = library
                elif ("HARDWARE SORT BIN" in current_line) and (dut_position in current_line):
                    #[2023-03-11 05:50:50:390][ANSKR22466158624000-1-11] HARDWARE SORT BIN = 1
                    tokens = current_line.split(']')
                    end_time = tokens[0].replace('[','')
                    if "HARDWARE SORT BIN = 1" in current_line:
                        print_item_dic['RESULT'] = "Pass"
                        pass_cnt = pass_cnt + 1
                       # print("{}, {},{}, pass".format(test_cnt,dut_position))
                    else:
                        print_item_dic['RESULT'] = "Fail"
                        fail_cnt = fail_cnt + 1
                        ttt = current_line
                        ttt = ttt.replace("\n","")
                        print("{}, {},{}, fail".format(test_cnt,dut_position,ttt))
                    break;
                elif ("]  Blade        :" in current_line) and (dut_position in current_line):
                    #[2023-03-11 05:49:13:245][ANSKR22466158624000-1-1]  Blade        : A03TW23095993211200
                    tokens = current_line.split(':')
                    tmp_str = tokens[4].replace('\n','')
                    print_item_dic['BLADE']=tmp_str
                elif ("]  ProtocolBoard:" in current_line) and (dut_position in current_line):
                    #[2023-03-11 05:49:13:245][ANSKR22466158624000-1-1]  Blade        : A03TW23095993211200
                    tokens = current_line.split(':')
                    tmp_str = tokens[4].replace('\n','')
                    print_item_dic['PB']=tmp_str
                elif ("]  xDP (Master) :" in current_line) and (dut_position in current_line):
                    #[2023-03-11 05:49:13:245][ANSKR22466158624000-1-1]  Blade        : A03TW23095993211200
                    tokens = current_line.split(':')
                    tmp_str = tokens[4].replace('\n','')
                    print_item_dic['DPS']=tmp_str
                elif ("]  Interposer   :" in current_line) and (dut_position in current_line):
                    #[2023-03-11 05:49:13:245][ANSKR22466158624000-1-1]  Blade        : A03TW23095993211200
                    tokens = current_line.split(':')
                    tmp_str = tokens[4].replace('\n','')
                    print_item_dic['INTERPOSER']=tmp_str
                elif ("]  TBSignal(DUT):" in current_line) and (dut_position in current_line):
                    #[2023-03-11 05:49:13:245][ANSKR22466158624000-1-1]  Blade        : A03TW23095993211200
                    tokens = current_line.split(':')
                    tmp_str = tokens[4].replace('\n','')
                    print_item_dic['TBSIGNAL']=tmp_str
                elif ("]  TBPower      :" in current_line) and (dut_position in current_line):
                    #[2023-03-11 05:49:13:245][ANSKR22466158624000-1-1]  Blade        : A03TW23095993211200
                    tokens = current_line.split(':')
                    tmp_str = tokens[4].replace('\n','')
                    print_item_dic['TBPOWER']=tmp_str
                elif ("] FATAL ERROR" in current_line) and (dut_position in current_line):
                    #[2023-06-27 17:34:46:528][ANSKR23036158601800-1-7] FATAL ERROR (0x825): ERROR: PCIe Link Width Fail ()
                    tokens = current_line.split(']')
                    tmp_str = tokens[2].replace('\n','')
                    existing_str = print_item_dic['FAIL_MSG']
                    existing_str = existing_str + "|" +tmp_str
                    print_item_dic['FAIL_MSG']=existing_str
                    print_item_dic['TEST_BLOCK'] = cur_test_block
                elif ("] ###" in current_line) and (dut_position in current_line):
                    #[2023-06-27 17:33:17:345][ANSKR23076158617000-1-3] ################## TestInit ##################
                    tokens = current_line.split(']')
                    tmp_str = tokens[2].replace('\n','')
                    tmp_str = tmp_str.replace('#','')
                    tmp_str = tmp_str.replace(' ','')
                    cur_test_block=tmp_str
                    #print(cur_test_block)
                current_line = logfile.readline()
            logfile.close()

            print_list.append(print_item_dic)

    # write a file 
    newFile = open(new_file_name, 'w', encoding='cp949')

    #test_cnt = pass_cnt + fail_cnt
    print('Pass : {}'.format(pass_cnt))
    print('Fail : {}'.format(fail_cnt))
    print('Test : {}'.format(test_cnt))

    newFile.write("RunID : {}\n".format(RunID))
    newFile.write("Recipe : {}\n".format(Recipe))
    newFile.write("exe : {}\n".format(exe))
    newFile.write("TestIN : {}\n".format(test_cnt))
    newFile.write("Passed : {}\n".format(pass_cnt))
    newFile.write("Failed : {}\n".format(fail_cnt))
    
    newFile.write('No, DUT, start time, blade, pb, dps,interposer, TB signal, TB power,test block, Fail Msg, result\n')
    for item in print_list:
        newFile.write("{},{},{},{},{},{},{},{},{},{},{},{}\n". \
        format(item['NO'],item['DUT'],item['START_TIME'], item['BLADE'], item['PB'],item['DPS'], item['INTERPOSER'],item['TBSIGNAL'],item['TBPOWER'],item['TEST_BLOCK'],item['FAIL_MSG'],item['RESULT']))
    newFile.close()