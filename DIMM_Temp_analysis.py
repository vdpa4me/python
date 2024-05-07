import sys
import os
from os.path import basename
import re

new_file_name = ''
new_file_names = []
g1_measurment_list = []
g2_measurment_list = []
g3_measurment_list = []
g4_measurment_list = []


if __name__ == '__main__':

    # get current directory 
    dir_name = os.path.dirname(os.path.realpath(__file__))

    # get failes in the current directory 
    file_list = []
    for (root, directories, files) in os.walk(dir_name):
        for file in files:
            file_path = os.path.join(root, file)
            path,ext = os.path.splitext(file_path)
            if ext in '.txt' :
                file_list.append(file_path)
    # list sort 
    file_list.sort()

    # new file for writing
    new_file_name = "output.csv"
    new_file_name = os.path.join(dir_name, new_file_name)

    # result_path = the current directory 
    result_path = dir_name

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
            elif "ELAPSE/TOTLDR" in current_line:
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

                for i in range(0, int(23)):
                    current_line = logfile.readline()
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
    with open(new_file_name, 'w') as f:
        f.write("ETERATION,CPU0_A_F,CPU0_G_L,CPU1_A_F,CPU1_G_L\n")
        for i in range(0, len(g1_measurment_list)):
            f.write(g1_measurment_list[i]['eteration'] + "," + str(g1_measurment_list[i]['DIFF']) + "," + str(g2_measurment_list[i]['DIFF']) + "," + str(g3_measurment_list[i]['DIFF']) + "," + str(g4_measurment_list[i]['DIFF']) + "\n")
        f.close()
    print("Output file: " + new_file_name)

