import sys
import os
from os.path import basename
import re

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
            if ext in '.log' :
                temp_dic = {}
                # new file for writing
                new_file_name = file+"_CPU.csv"
                new_file_name = os.path.join(dir_name, new_file_name)
                temp_dic['read'] = file_path
                temp_dic['write']= new_file_name
                file_list.append(temp_dic)

    for file_dic in file_list:
        read_file = file_dic['read']
        write_file = file_dic['write']
        
        cpu0_temp_list = []
        cpu0_power_list = []
        cpu1_temp_list = []
        cpu1_power_list = []

        cmb_num = 0
        if "CMB1_" in read_file:
            cmb_num = 1
        elif "CMB2_" in read_file:
            cmb_num = 2
        elif "CMB3_" in read_file:
            cmb_num = 3
        elif "CMB4_" in read_file:
            cmb_num = 4
        elif "CMB5_" in read_file:
            cmb_num = 5
        elif "CMB6_" in read_file:
            cmb_num = 6
        elif "CMB7_" in read_file:
            cmb_num = 7
        elif "CMB8_" in read_file:
            cmb_num = 8
        elif "CMB9_" in read_file:
            cmb_num = 9
        elif "CMB10_" in read_file:
            cmb_num = 10
        elif "CMB11_" in read_file:
            cmb_num = 11
        elif "CMB12_" in read_file:
            cmb_num = 12

        # initial read
        logfile = open(read_file, 'r', encoding='utf8', errors='ignore')
        current_line = logfile.readline()
        dut_list = []

        isCPULog = False
     
        print (cmb_num)
        while current_line:
            # Skip empty line
            
            if "CPU0" in current_line:
                new_source = ' '.join(current_line.split())
                new_source = new_source.replace(' ', ',')   
                #0,1   ,2,3,4   , 5  ,6,   7 ,8,9 ,10    ,11  ,12  ,13  ,14  ,15,16,17,18,19,20    ,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55  
                #0,CPU0,-,-,1785,1567,1,74.91,3.99,100.00,0.00,0.00,0.00,0.00,- ,- ,- ,57,45,360.02,0.691,0.707,0x0,0x0,0,37.469,37.469
                tokens = new_source.split(',')
                temp = tokens[17]
                power = tokens[19]
                print("CPU0 - TEMP: " + temp + " POWER: " + power +"\n")
                tempval = int(temp)
                powerval = float(power)    
                cpu0_temp_list.append(tempval)
                cpu0_power_list.append(powerval)
              
            elif "CPU1" in current_line:
                new_source = ' '.join(current_line.split())
                new_source = new_source.replace(' ', ',')   
                #0,1   ,2,3,4   , 5  ,6,   7 ,8,9 ,10    ,11  ,12  ,13  ,14  ,15,16,17,18,19,20    ,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55  
                #0,CPU0,-,-,1785,1567,1,74.91,3.99,100.00,0.00,0.00,0.00,0.00,- ,- ,- ,57,45,360.02,0.691,0.707,0x0,0x0,0,37.469,37.469
                tokens = new_source.split(',')
                temp = tokens[17]
                power = tokens[19]
                print("CPU1 - TEMP: " + temp + " POWER: " + power +"\n")
                tempval = int(temp)
                powerval = float(power)    
                cpu1_temp_list.append(tempval)
                cpu1_power_list.append(powerval)
            current_line = logfile.readline()

            
        # write to csv
        with open(write_file, 'w') as f:
            f.write("##############################################\n")
            f.write("1. CPU Temperature / Power Watt. \n")
            f.write("##############################################\n")
            f.write("\n")
            
            max_cpu0_temp = 0
            sum_cpu0_temp = 0    
            sum_cpu0_power = 0
            cpu0_mesurement_cnt = 0  

            max_cpu1_temp = 0
            sum_cpu1_temp = 0    
            sum_cpu1_power = 0
            cpu1_mesurement_cnt = 0  

            if(len(cpu0_temp_list) == len(cpu0_power_list)):
                f.write("CMB#, Index, CPU0 Temperature , CPU0 Power, CPU1 Temperature, CPU1 Power\n")
                for i in range(0, len(cpu0_temp_list)):
                    cpu0_mesurement_cnt += 1
                    if max_cpu0_temp < int(cpu0_temp_list[i]):
                        max_cpu0_temp = int(cpu0_temp_list[i])
                    sum_cpu0_temp += int(cpu0_temp_list[i])   
                    sum_cpu0_power += float(cpu0_power_list[i])

                    cpu1_mesurement_cnt += 1
                    if max_cpu1_temp < int(cpu1_temp_list[i]):
                        max_cpu1_temp = int(cpu1_temp_list[i])
                    sum_cpu1_temp += int(cpu1_temp_list[i])   
                    sum_cpu1_power += float(cpu1_power_list[i])
                    f.write(str(cmb_num)+","+str(cpu0_mesurement_cnt)+","+str(cpu0_temp_list[i]) + "," + str(cpu0_power_list[i])+ ","+str(cpu1_temp_list[i]) + "," + str(cpu1_power_list[i]) +"\n")
                
                
                f.write("CPU0 MAX TMP(C)"+ "," + str(max_cpu0_temp) + "\n")
                f.write("CPU0 AVG TMP(C)"+ "," + str(round(sum_cpu0_temp/cpu0_mesurement_cnt)) + "\n")
                f.write("CPU0 AVG PWR(Watt.)"+ "," + str(round(sum_cpu0_power/cpu0_mesurement_cnt)) + "\n")
                
                f.write("CPU1 MAX TMP(C)"+ "," + str(max_cpu1_temp) + "\n")
                f.write("CPU1 AVG TMP(C)"+ "," + str(round(sum_cpu1_temp/cpu1_mesurement_cnt)) + "\n")
                f.write("CPU1 AVG PWR(Watt.)"+ "," + str(round(sum_cpu1_power/cpu1_mesurement_cnt)) + "\n")

                cpu_max_temp_dic = {}
                cpu_max_temp_dic['CMB'] = cmb_num
                cpu_max_temp_dic['cpu0_max_temp'] = max_cpu0_temp
                cpu_max_temp_dic['cpu1_max_temp'] = max_cpu1_temp
                report_list.append(cpu_max_temp_dic)
                
            else:
                f.write("CMB#, CPU#, Index, Temperature , Power\n")
                for i in range(0, len(cpu0_temp_list)):
                    cpu0_mesurement_cnt += 1
                    if max_cpu0_temp < int(cpu0_temp_list[i]):
                        max_cpu0_temp = int(cpu0_temp_list[i])
                    sum_cpu0_temp += int(cpu0_temp_list[i])   
                    sum_cpu0_power += float(cpu0_power_list[i])
                    f.write(str(cmb_num)+",0,"+str(cpu0_mesurement_cnt)+","+str(cpu0_temp_list[i]) + "," + str(cpu0_power_list[i]) +"\n")
    

                f.write("CPU0 MAX TMP(C)"+ "," + str(max_cpu0_temp) + "\n")
                f.write("CPU0 AVG TMP(C)"+ "," + str(round(sum_cpu0_temp/cpu0_mesurement_cnt)) + "\n")
                f.write("CPU0 AVG PWR(Watt.)"+ "," + str(round(sum_cpu0_power/cpu0_mesurement_cnt)) + "\n")

                
                f.write("\n")
                f.write("\n")
                f.write("\n")
                f.write("CMB#, CPU#, Index, Temperature , Power\n")

                for i in range(0, len(cpu1_temp_list)):
                    cpu1_mesurement_cnt += 1
                    if max_cpu1_temp < int(cpu1_temp_list[i]):
                        max_cpu1_temp = int(cpu1_temp_list[i])
                    sum_cpu1_temp += int(cpu1_temp_list[i])   
                    sum_cpu1_power += float(cpu1_power_list[i])
                    f.write(str(cmb_num)+",1,"+str(cpu0_mesurement_cnt)+","+str(cpu0_temp_list[i]) + "," + str(cpu0_power_list[i]) +"\n")            

                f.write("CPU1 MAX TMP(C)"+ "," + str(max_cpu1_temp) + "\n")
                f.write("CPU1 AVG TMP(C)"+ "," + str(round(sum_cpu1_temp/cpu1_mesurement_cnt)) + "\n")
                f.write("CPU1 AVG PWR(Watt.)"+ "," + str(round(sum_cpu1_power/cpu1_mesurement_cnt)) + "\n")

                cpu_max_temp_dic = {}
                cpu_max_temp_dic['CMB'] = cmb_num
                cpu_max_temp_dic['cpu0_max_temp'] = max_cpu0_temp
                cpu_max_temp_dic['cpu1_max_temp'] = max_cpu1_temp
                report_list.append(cpu_max_temp_dic)

        f.close()

    # wirte to report
    with open("TotalReportCPU.csv", 'w') as rf:
        rf.write("##############################################\n")
        rf.write("1. CPU MAX TEMP\n")
        rf.write("##############################################\n")
        rf.write("\n")
        rf.write("CMB# ,CPU0 MAX TMP, CPU1 MAX TMP\n")
        report_list.sort(key=lambda x: x['CMB'], reverse=True)
        for i in range(0, len(report_list)):
            cpu_max_temp_dic = report_list[i]
            rf.write(str(cpu_max_temp_dic['CMB'])+","+str(cpu_max_temp_dic['cpu0_max_temp'])+","+str(cpu_max_temp_dic['cpu1_max_temp'])+"\n")
        rf.write("\n")
        rf.close()
    


