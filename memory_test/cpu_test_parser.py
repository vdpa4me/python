import sys
import os
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
        
        cpu_temp_list = []
        cpu_power_list = []
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
            
            if "S0-CPU_Temp" in current_line:
                 isCPULog = True
            elif "," in current_line and isCPULog == True:
                tokens = current_line.split(',')
                if len(tokens) < 14:
                    continue
                temp = tokens[11]
                power = tokens[13]
                #print("TEMP: " + temp + " POWER: " + power )
                cpu_temp_list.append(temp)
                cpu_power_list.append(power)
                
            current_line = logfile.readline()
        logfile.close()

        # write to csv
        with open(write_file, 'w') as f:
            f.write("##############################################\n")
            f.write("1. CPU Temperature / Power Watt. \n")
            f.write("##############################################\n")
            f.write("\n")
            
            max_cpu_temp = 0
            sum_cpu_temp = 0    
            sum_cpu_power = 0
            cpu_mesurement_cnt = 0  
            f.write("CMB#,Index, CPU Temperature,CPU Power\n")
            for i in range(0, len(cpu_temp_list)):
                cpu_mesurement_cnt += 1
                if max_cpu_temp < int(cpu_temp_list[i]):
                    max_cpu_temp = int(cpu_temp_list[i])
                sum_cpu_temp += int(cpu_temp_list[i])   
                sum_cpu_power += float(cpu_power_list[i])
                f.write(str(cmb_num)+","+str(cpu_mesurement_cnt)+","+cpu_temp_list[i] + "," + cpu_power_list[i] + "\n")

            f.write("MAX TRMP(C)"+ "," + str(max_cpu_temp) + "," + "N/A" + "\n")
            f.write("AVG TEMP(C)/AVG Power(Watt.)"+ "," + str(round(sum_cpu_temp/cpu_mesurement_cnt)) + "," + str(round(sum_cpu_power/cpu_mesurement_cnt)) + "\n")
            f.write("\n")
            cpu_max_temp_dic = {}
            cpu_max_temp_dic['CMB'] = cmb_num
            cpu_max_temp_dic['max_temp'] = max_cpu_temp
            report_list.append(cpu_max_temp_dic)

        f.close()

    # wirte to report
    with open("TotalReportCPU.csv", 'w') as rf:
        rf.write("##############################################\n")
        rf.write("1. CPU MAX TEMP\n")
        rf.write("##############################################\n")
        rf.write("\n")
        rf.write("CMB,MAX CPU \n")
        report_list.sort(key=lambda x: x['CMB'], reverse=True)
        for i in range(0, len(report_list)):
            cpu_max_temp_dic = report_list[i]
            rf.write(str(cpu_max_temp_dic['CMB'])+","+str(cpu_max_temp_dic['max_temp'])+"\n")
        rf.write("\n")
        rf.close()
    


