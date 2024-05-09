import sys
import os
from os.path import basename
import re



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
                new_file_name = file+"_DIMM_CPU.csv"
                new_file_name = os.path.join(dir_name, new_file_name)
                temp_dic['read'] = file_path
                temp_dic['write']= new_file_name
                file_list.append(temp_dic)


    # result_path = the current directory 
    result_path = dir_name

    for file_dic in file_list:
        read_file = file_dic['read']
        write_file = file_dic['write']

        g1_measurment_list = []
        g2_measurment_list = []
        g3_measurment_list = []
        g4_measurment_list = []

        isDimmTest = False
        isCPUTest = False

        cpu_temp_list = []
        cpu_power_list = []

        # initial read
        logfile = open(read_file, 'r', encoding='utf8', errors='ignore')
        current_line = logfile.readline()
        dut_list = []

        while current_line:
            # Skip empty line
            if current_line == '\n':
                current_line = logfile.readline()
                continue
            elif "### DIMMTEMP_START ###" in current_line:
                isDimmTest = True
            elif "### DIMMTEMP_END ###" in current_line:
                isDimmTest = False
            elif "### CPUTEMP_START ###" in current_line:
                 while(True):
                    current_line = logfile.readline()
                    if "S0-CPU_Temp" in current_line:
                        continue

                    elif "," in current_line:
                        tokens = current_line.split(',')
                        if len(tokens) < 14:
                            continue
                        temp = tokens[11]
                        power = tokens[13]
                        print("TEMP: " + temp + " POWER: " + power )
                        cpu_temp_list.append(temp)
                        cpu_power_list.append(power)
                        continue
                    elif "### CPUTEMP_END ###" in current_line:
                        break
            elif "ELAPSE/TOTLDR" in current_line and isDimmTest == True:
                #ELAPSE/TOTLDR = 20/900
                tokens = current_line.split('=')
                eteration = tokens[1]
                eteration = eteration.replace('\n','')
                temp_grp1_dic = {}
                temp_grp2_dic = {}
                temp_grp3_dic = {}
                temp_grp4_dic = {}
                temp_grp1_dic['eteration'] = eteration
                temp_grp2_dic['eteration'] = eteration
                temp_grp3_dic['eteration'] = eteration
                temp_grp4_dic['eteration'] = eteration

                g1minVal = 0
                g2minVal = 0
                g3minVal = 0
                g4minVal = 0

                g1maxVal = 0
                g2maxVal = 0
                g3maxVal = 0
                g4maxVal = 0

                g1sumVal = 0
                g2sumVal = 0
                g3sumVal = 0
                g4sumVal = 0

                g1cntVal = 0
                g2cntVal = 0
                g3cntVal = 0
                g4cntVal = 0

                dimm_cnt = 0
                #for i in range(0, int(23)):
                while(dimm_cnt < 24):
                    current_line = logfile.readline()
                    tmpstr = current_line
                    tmpstr = tmpstr.replace('\n','')
                    tmpstr = tmpstr.replace(' ','')
                    if len(tmpstr) == 0:
                        continue
                    dimm_cnt += 1
                    #print (str(dimm_cnt) + " : "+ current_line)

                    tokens = current_line.split('|')
                    DIMMNO = tokens[0]
                    DIMMTEMP = tokens[1]
                    DIMMTEMP = DIMMTEMP.replace(' degrees C','')
                    DIMMTEMPVal = int(DIMMTEMP)
                    temp_dic = {}
                    temp_dic['DIMMNO'] = DIMMNO
                    temp_dic['DIMMTEMP'] = DIMMTEMPVal 
                    if "CPU0_DIMM_TEMP_A" in DIMMNO or "CPU0_DIMM_TEMP_B" in DIMMNO or "CPU0_DIMM_TEMP_C" in DIMMNO or "CPU0_DIMM_TEMP_D" in DIMMNO or "CPU0_DIMM_TEMP_E" in DIMMNO or "CPU0_DIMM_TEMP_F" in DIMMNO:
                        temp_grp1_dic[DIMMNO] = temp_dic
                        g1sumVal += DIMMTEMPVal
                        g1cntVal += 1
                        if g1minVal == 0:
                            g1minVal = DIMMTEMPVal
                            g1maxVal = DIMMTEMPVal
                        else:
                            if DIMMTEMPVal < g1minVal:
                                g1minVal = DIMMTEMPVal
                            if DIMMTEMPVal > g1maxVal:
                                g1maxVal = DIMMTEMPVal
                        #print("GROUP1: " + DIMMNO + " " + DIMMTEMP)
                    elif "CPU0_DIMM_TEMP_G" in DIMMNO or "CPU0_DIMM_TEMP_H" in DIMMNO or "CPU0_DIMM_TEMP_I" in DIMMNO or "CPU0_DIMM_TEMP_J" in DIMMNO or "CPU0_DIMM_TEMP_K" in DIMMNO or "CPU0_DIMM_TEMP_L" in DIMMNO:
                        temp_grp2_dic[DIMMNO] = temp_dic
                        g2sumVal += DIMMTEMPVal
                        g2cntVal += 1
                        if g2minVal == 0:
                            g2minVal = DIMMTEMPVal
                            g2maxVal = DIMMTEMPVal
                        else:
                            if DIMMTEMPVal < g2minVal:
                                g2minVal = DIMMTEMPVal
                            if DIMMTEMPVal > g2maxVal:
                                g2maxVal = DIMMTEMPVal
                        #print("GROUP2: " + DIMMNO + " " + DIMMTEMP)
                    elif "CPU1_DIMM_TEMP_A" in DIMMNO or "CPU1_DIMM_TEMP_B" in DIMMNO or "CPU1_DIMM_TEMP_C" in DIMMNO or "CPU1_DIMM_TEMP_D" in DIMMNO or "CPU1_DIMM_TEMP_E" in DIMMNO or "CPU1_DIMM_TEMP_F" in DIMMNO:
                        temp_grp3_dic[DIMMNO] = temp_dic
                        g3sumVal += DIMMTEMPVal
                        g3cntVal += 1
                        if g3minVal == 0:
                            g3minVal = DIMMTEMPVal
                            g3maxVal = DIMMTEMPVal
                        else:
                            if DIMMTEMPVal < g3minVal:
                                g3minVal = DIMMTEMPVal
                            if DIMMTEMPVal > g3maxVal:
                                g3maxVal = DIMMTEMPVal
                        #print("GROUP3: " + DIMMNO + " " + DIMMTEMP)
                    elif "CPU1_DIMM_TEMP_G" in DIMMNO or "CPU1_DIMM_TEMP_H" in DIMMNO or "CPU1_DIMM_TEMP_I" in DIMMNO or "CPU1_DIMM_TEMP_J" in DIMMNO or "CPU1_DIMM_TEMP_K" in DIMMNO or "CPU1_DIMM_TEMP_L" in DIMMNO:
                        temp_grp4_dic[DIMMNO] = temp_dic
                        g4sumVal += DIMMTEMPVal
                        g4cntVal += 1
                        if g4minVal == 0:
                            g4minVal = DIMMTEMPVal
                            g4maxVal = DIMMTEMPVal
                        else:
                            if DIMMTEMPVal < g4minVal:
                                g4minVal = DIMMTEMPVal
                            if DIMMTEMPVal > g4maxVal:
                                g4maxVal = DIMMTEMPVal
                        #print("GROUP4: " + DIMMNO + " " + DIMMTEMP)
                temp_grp1_dic['MIN'] = g1minVal
                temp_grp1_dic['MAX'] = g1maxVal
                temp_grp1_dic['DIFF'] = g1maxVal - g1minVal

                temp_grp2_dic['MIN'] = g2minVal
                temp_grp2_dic['MAX'] = g2maxVal
                temp_grp2_dic['DIFF'] = g2maxVal - g2minVal

                temp_grp3_dic['MIN'] = g3minVal
                temp_grp3_dic['MAX'] = g3maxVal
                temp_grp3_dic['DIFF'] = g3maxVal - g3minVal

                temp_grp4_dic['MIN'] = g4minVal
                temp_grp4_dic['MAX'] = g4maxVal
                temp_grp4_dic['DIFF'] = g4maxVal - g4minVal

                g1_measurment_list.append(temp_grp1_dic)
                g2_measurment_list.append(temp_grp2_dic)
                g3_measurment_list.append(temp_grp3_dic)
                g4_measurment_list.append(temp_grp4_dic)



                #print(eteration + ": G1MIN:"+ str(g1minVal) +" G1MAX:"+ str(g1maxVal) +" G1DIFF:"+ str(g1maxVal - g1minVal))
                #print(eteration + ": G2MIN:"+ str(g2minVal) +" G1MAX:"+ str(g2maxVal) +" G1DIFF:"+ str(g2maxVal - g2minVal))
                #print(eteration + ": G3MIN:"+ str(g3minVal) +" G1MAX:"+ str(g3maxVal) +" G1DIFF:"+ str(g3maxVal - g3minVal))
                #print(eteration + ": G4MIN:"+ str(g4minVal) +" G1MAX:"+ str(g4maxVal) +" G1DIFF:"+ str(g4maxVal - g4minVal))
                
            current_line = logfile.readline()
        logfile.close()

        # write to csv
        with open(write_file, 'w') as f:
            f.write("##############################################\n")
            f.write("1. DIMM Temperature Uniformity \n")
            f.write("##############################################\n")
            f.write("\n")
            f.write("ETERATION,CPU0_A_F,CPU0_G_L,CPU1_A_F,CPU1_G_L\n")
            g1_diff_min_val = 0
            g2_diff_min_val = 0
            g3_diff_min_val = 0
            g4_diff_min_val = 0

            g1_diff_max_val = 0
            g2_diff_max_val = 0
            g3_diff_max_val = 0
            g4_diff_max_val = 0

            g1_diff_sum_val = 0
            g2_diff_sum_val = 0
            g3_diff_sum_val = 0
            g4_diff_sum_val = 0

            g1_diff_cnt_val = 0
            g2_diff_cnt_val = 0
            g3_diff_cnt_val = 0
            g4_diff_cnt_val = 0
            
           
            for i in range(0, len(g1_measurment_list)):
                f.write(g1_measurment_list[i]['eteration'] + "," + str(g1_measurment_list[i]['DIFF']) + "," + str(g2_measurment_list[i]['DIFF']) + "," + str(g3_measurment_list[i]['DIFF']) + "," + str(g4_measurment_list[i]['DIFF']) + "\n")
                #g1
                if g1_diff_min_val == 0:
                    g1_diff_min_val = g1_measurment_list[i]['DIFF']
                else:
                    if g1_measurment_list[i]['DIFF'] < g1_diff_min_val:
                        g1_diff_min_val = g1_measurment_list[i]['DIFF']
                if g1_measurment_list[i]['DIFF'] > g1_diff_max_val:
                    g1_diff_max_val = g1_measurment_list[i]['DIFF']
                g1_diff_sum_val = g1_diff_sum_val + g1_measurment_list[i]['DIFF']
                g1_diff_cnt_val = g1_diff_cnt_val + 1

                #g2
                if g2_diff_min_val == 0:
                    g2_diff_min_val = g2_measurment_list[i]['DIFF']
                else:
                    if g2_measurment_list[i]['DIFF'] < g2_diff_min_val:
                        g2_diff_min_val = g2_measurment_list[i]['DIFF']
                if g2_measurment_list[i]['DIFF'] > g2_diff_max_val:
                    g2_diff_max_val = g2_measurment_list[i]['DIFF']
                g2_diff_sum_val = g2_diff_sum_val + g2_measurment_list[i]['DIFF']
                g2_diff_cnt_val = g2_diff_cnt_val + 1

                #g3 
                if g3_diff_min_val == 0:
                    g3_diff_min_val = g3_measurment_list[i]['DIFF']
                else:
                    if g3_measurment_list[i]['DIFF'] < g3_diff_min_val:
                        g3_diff_min_val = g3_measurment_list[i]['DIFF']
                if g3_measurment_list[i]['DIFF'] > g3_diff_max_val:
                    g3_diff_max_val = g3_measurment_list[i]['DIFF']
                g3_diff_sum_val = g3_diff_sum_val + g3_measurment_list[i]['DIFF']
                g3_diff_cnt_val = g3_diff_cnt_val + 1

                #g4
                if g4_diff_min_val == 0:
                    g4_diff_min_val = g4_measurment_list[i]['DIFF']
                else:
                    if g4_measurment_list[i]['DIFF'] < g4_diff_min_val:
                        g4_diff_min_val = g4_measurment_list[i]['DIFF']
                if g4_measurment_list[i]['DIFF'] > g4_diff_max_val:
                    g4_diff_max_val = g4_measurment_list[i]['DIFF']
                g4_diff_sum_val = g4_diff_sum_val + g4_measurment_list[i]['DIFF']
                g4_diff_cnt_val = g4_diff_cnt_val + 1
            
            f.write("MAX"+ "," + str(g1_diff_max_val) + "," + str(g2_diff_max_val) + "," + str(g3_diff_max_val) + "," + str(g4_diff_max_val) + "\n")
            f.write("MIN"+ "," + str(g1_diff_min_val) + "," + str(g2_diff_min_val) + "," + str(g3_diff_min_val) + "," + str(g4_diff_min_val) + "\n")
            f.write("AVG"+ "," + str(round(g1_diff_sum_val/g1_diff_cnt_val)) + "," + str(round(g2_diff_sum_val/g2_diff_cnt_val)) + "," + str(round(g3_diff_sum_val/g3_diff_cnt_val)) + "," + str(round(g4_diff_sum_val/g4_diff_cnt_val)) + "\n")
            f.write("\n")
            f.write("\n")
            f.write("##############################################\n")
            f.write("2. CPU Temperature / Power Watt. \n")
            f.write("##############################################\n")
            f.write("\n")
            
            max_cpu_temp = 0
            sum_cpu_temp = 0    
            sum_cpu_power = 0
            cpu_mesurement_cnt = 0  
            f.write("Index, CPU Temperature,CPU Power\n")
            for i in range(0, len(cpu_temp_list)):
                cpu_mesurement_cnt += 1
                if max_cpu_temp < int(cpu_temp_list[i]):
                    max_cpu_temp = int(cpu_temp_list[i])
                sum_cpu_temp += int(cpu_temp_list[i])   
                sum_cpu_power += float(cpu_power_list[i])
                f.write(str(cpu_mesurement_cnt)+","+cpu_temp_list[i] + "," + cpu_power_list[i] + "\n")

            f.write("MAX"+ "," + str(max_cpu_temp) + "," + "N/A" + "\n")
            f.write("AVG"+ "," + str(round(sum_cpu_temp/cpu_mesurement_cnt)) + "," + str(round(sum_cpu_power/cpu_mesurement_cnt)) + "\n")


            f.close()
    

