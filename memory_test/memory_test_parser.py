import sys
import os
from os.path import basename

target_iteration = "800/900"
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
                new_file_name = file+"_DIMM.csv"
                new_file_name = os.path.join(dir_name, new_file_name)
                temp_dic['read'] = file_path
                temp_dic['write']= new_file_name
                file_list.append(temp_dic)

    for file_dic in file_list:
        read_file = file_dic['read']
        write_file = file_dic['write']

        total_measurment_list = []

        isDimmTest = False

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
     
        while current_line:
            # Skip empty line
            if "ELAPSE/TOTLDR" in current_line:
                #ELAPSE/TOTLDR = 20/900
                iteration_dic = {}
 
                tokens = current_line.split('=')
                iteration = tokens[1]
                iteration = iteration.replace('\n','')
                iteration = iteration.replace(' ','')

                iteration_dic['iteration'] = iteration
                group1_dic = {}
                group2_dic = {}
                group3_dic = {}
                group4_dic = {}

                g1minVal = 0
                g1maxVal = 0
                g2minVal = 0
                g2maxVal = 0
                g3minVal = 0
                g3maxVal = 0
                g4minVal = 0
                g4maxVal = 0

                dimm_cnt = 0
                while(dimm_cnt < 24):
                    current_line = logfile.readline()
                    if "CPU0_" not in current_line and "CPU1_" not in current_line:
                        continue
                    dimm_cnt += 1
                   
                    tokens = current_line.split('|')
                    DIMMNO = tokens[0]
                    DIMMTEMP = tokens[1]
                    DIMMTEMP = DIMMTEMP.replace(' degrees C','')
                    DIMMTEMPVal = int(DIMMTEMP)


                    cur_grp_no = 0

                  
                    if "CPU0_DIMM_TEMP_A" in DIMMNO:
                        group1_dic['A'] = DIMMTEMPVal
                        cur_grp_no = 1
                    elif "CPU0_DIMM_TEMP_B" in DIMMNO:
                        group1_dic['B'] = DIMMTEMPVal
                        cur_grp_no = 1
                    elif "CPU0_DIMM_TEMP_C" in DIMMNO:
                        group1_dic['C'] = DIMMTEMPVal
                        cur_grp_no = 1
                    elif "CPU0_DIMM_TEMP_D" in DIMMNO:
                        group1_dic['D'] = DIMMTEMPVal
                        cur_grp_no = 1
                    elif "CPU0_DIMM_TEMP_E" in DIMMNO:
                        group1_dic['E'] = DIMMTEMPVal
                        cur_grp_no = 1
                    elif "CPU0_DIMM_TEMP_F" in DIMMNO:
                        group1_dic['F'] = DIMMTEMPVal
                        cur_grp_no = 1

                    elif "CPU0_DIMM_TEMP_G" in DIMMNO:
                        group2_dic['G'] = DIMMTEMPVal
                        cur_grp_no = 2
                    elif "CPU0_DIMM_TEMP_H" in DIMMNO:
                        group2_dic['H'] = DIMMTEMPVal
                        cur_grp_no = 2
                    elif "CPU0_DIMM_TEMP_I" in DIMMNO:
                        group2_dic['I'] = DIMMTEMPVal
                        cur_grp_no = 2
                    elif "CPU0_DIMM_TEMP_J" in DIMMNO:
                        group2_dic['J'] = DIMMTEMPVal
                        cur_grp_no = 2
                    elif "CPU0_DIMM_TEMP_K" in DIMMNO:
                        group2_dic['K'] = DIMMTEMPVal
                        cur_grp_no = 2
                    elif "CPU0_DIMM_TEMP_L" in DIMMNO:
                        group2_dic['L'] = DIMMTEMPVal
                        cur_grp_no = 2

                    elif "CPU1_DIMM_TEMP_A" in DIMMNO:
                        group3_dic['A'] = DIMMTEMPVal
                        cur_grp_no = 3
                    elif "CPU1_DIMM_TEMP_B" in DIMMNO:
                        group3_dic['B'] = DIMMTEMPVal
                        cur_grp_no = 3
                    elif "CPU1_DIMM_TEMP_C" in DIMMNO:
                        group3_dic['C'] = DIMMTEMPVal
                        cur_grp_no = 3
                    elif "CPU1_DIMM_TEMP_D" in DIMMNO:
                        group3_dic['D'] = DIMMTEMPVal
                        cur_grp_no = 3
                    elif "CPU1_DIMM_TEMP_E" in DIMMNO:
                        group3_dic['E'] = DIMMTEMPVal
                        cur_grp_no = 3
                    elif "CPU1_DIMM_TEMP_F" in DIMMNO:
                        group3_dic['F'] = DIMMTEMPVal
                        cur_grp_no = 3

                    elif "CPU1_DIMM_TEMP_G" in DIMMNO:
                        group4_dic['G'] = DIMMTEMPVal
                        cur_grp_no = 4
                    elif "CPU1_DIMM_TEMP_H" in DIMMNO:
                        group4_dic['H'] = DIMMTEMPVal
                        cur_grp_no = 4
                    elif "CPU1_DIMM_TEMP_I" in DIMMNO:
                        group4_dic['I'] = DIMMTEMPVal
                        cur_grp_no = 4
                    elif "CPU1_DIMM_TEMP_J" in DIMMNO:
                        group4_dic['J'] = DIMMTEMPVal
                        cur_grp_no = 4
                    elif "CPU1_DIMM_TEMP_K" in DIMMNO:
                        group4_dic['K'] = DIMMTEMPVal
                        cur_grp_no = 4
                    elif "CPU1_DIMM_TEMP_L" in DIMMNO:
                        group4_dic['L'] = DIMMTEMPVal
                        cur_grp_no = 4
                
                    if(cur_grp_no == 1):
                        if g1minVal == 0:
                            g1minVal = DIMMTEMPVal
                            g1maxVal = DIMMTEMPVal
                        else:
                            if DIMMTEMPVal < g1minVal:
                                g1minVal = DIMMTEMPVal
                            if DIMMTEMPVal > g1maxVal:
                                g1maxVal = DIMMTEMPVal
                    elif(cur_grp_no == 2):
                        if g2minVal == 0:
                            g2minVal = DIMMTEMPVal
                            g2maxVal = DIMMTEMPVal
                        else:
                            if DIMMTEMPVal < g2minVal:
                                g2minVal = DIMMTEMPVal
                            if DIMMTEMPVal > g2maxVal:
                                g2maxVal = DIMMTEMPVal
                    elif(cur_grp_no == 3):
                        if g3minVal == 0:
                            g3minVal = DIMMTEMPVal
                            g3maxVal = DIMMTEMPVal
                        else:
                            if DIMMTEMPVal < g3minVal:
                                g3minVal = DIMMTEMPVal
                            if DIMMTEMPVal > g3maxVal:
                                g3maxVal = DIMMTEMPVal
                    elif(cur_grp_no == 4):
                        if g4minVal == 0:
                            g4minVal = DIMMTEMPVal
                            g4maxVal = DIMMTEMPVal
                        else:
                            if DIMMTEMPVal < g4minVal:
                                g4minVal = DIMMTEMPVal
                            if DIMMTEMPVal > g4maxVal:
                                g4maxVal = DIMMTEMPVal
                    else:
                        print("ERROR: " + DIMMNO)
                        exit(1)

                group1_dic['MIN'] = g1minVal
                group1_dic['MAX'] = g1maxVal
                group1_dic['DIFF'] = g1maxVal - g1minVal

                group2_dic['MIN'] = g2minVal
                group2_dic['MAX'] = g2maxVal
                group2_dic['DIFF'] = g2maxVal - g2minVal

                group3_dic['MIN'] = g3minVal
                group3_dic['MAX'] = g3maxVal
                group3_dic['DIFF'] = g3maxVal - g3minVal

                group4_dic['MIN'] = g4minVal
                group4_dic['MAX'] = g4maxVal
                group4_dic['DIFF'] = g4maxVal - g4minVal

                iteration_dic['g1'] = group1_dic
                iteration_dic['g2'] = group2_dic
                iteration_dic['g3'] = group3_dic
                iteration_dic['g4'] = group4_dic

                total_measurment_list.append(iteration_dic)

                if target_iteration in iteration:
                    print("Target iteration found: " + target_iteration)
                    report_dic = {}
                    report_dic['CMB'] = cmb_num
                    report_dic['value'] = iteration_dic
                    report_list.append(report_dic)
                    
            current_line = logfile.readline()
        logfile.close()

        # write to csv
        with open(write_file, 'w') as f:
            f.write("##############################################\n")
            f.write("1. DIMM Temperature Uniformity \n")
            f.write("##############################################\n")
            f.write("\n")
            f.write("Iteration,CPU1_F,CPU1_E,CPU1_D,CPU1_C,CPU1_B,CPU1_A,G3_MIN,G3_MAX,G3_DIFF,\
                              ,CPU1_G,CPU1_H,CPU1_I,CPU1_J,CPU1_K,CPU1_L,G4_MIN,G4_MAX,G4_DIFF,\
                              ,CPU0_F,CPU0_E,CPU0_D,CPU0_C,CPU0_B,CPU0_A,G1_MIN,G1_MAX,G1_DIFF,\
                              ,CPU0_G,CPU0_H,CPU0_I,CPU0_J,CPU0_K,CPU0_L,G2_MIN,G2_MAX,G2_DIFF \n")
                       
            for i in range(0, len(total_measurment_list)):
                iteration = total_measurment_list[i]['iteration'] 
                group1_dic = total_measurment_list[i]['g1']
                group2_dic = total_measurment_list[i]['g2']
                group3_dic = total_measurment_list[i]['g3']
                group4_dic = total_measurment_list[i]['g4']

                f.write(iteration+","+str(group3_dic['F'])+","+str(group3_dic['E'])+","+str(group3_dic['D'])+","+str(group3_dic['C'])+","+str(group3_dic['B'])+","+str(group3_dic['A'])+ \
                                  ","+str(group3_dic['MIN'])+","+str(group3_dic['MAX'])+","+str(group3_dic['DIFF'])+","+ \
                                  ","+str(group4_dic['G'])+","+str(group4_dic['H'])+","+str(group4_dic['I'])+","+str(group4_dic['J'])+","+str(group4_dic['K'])+","+str(group4_dic['L'])+ \
                                  ","+str(group4_dic['MIN'])+","+str(group4_dic['MAX'])+","+str(group4_dic['DIFF'])+","+ \
                                  ","+str(group1_dic['F'])+","+str(group1_dic['E'])+","+str(group1_dic['D'])+","+str(group1_dic['C'])+","+str(group1_dic['B'])+","+str(group1_dic['A'])+ \
                                  ","+str(group1_dic['MIN'])+","+str(group1_dic['MAX'])+","+str(group1_dic['DIFF'])+","+ \
                                  ","+str(group2_dic['G'])+","+str(group2_dic['H'])+","+str(group2_dic['I'])+","+str(group2_dic['J'])+","+str(group2_dic['K'])+","+str(group2_dic['L'])+ \
                                  ","+str(group2_dic['MIN'])+","+str(group2_dic['MAX'])+","+str(group2_dic['DIFF'])+"\n")
            f.write("\n")
            f.close()
    

    # wirte to report
    with open("TotalReport.csv", 'w') as rf:
        rf.write("##############################################\n")
        rf.write("1. DIMM Temperature Uniformity \n")
        rf.write("##############################################\n")
        rf.write("\n")
        rf.write("CMB,Iteration,CPU1_F,CPU1_E,CPU1_D,CPU1_C,CPU1_B,CPU1_A,G3_MIN,G3_MAX,G3_DIFF,\
                            ,CPU1_G,CPU1_H,CPU1_I,CPU1_J,CPU1_K,CPU1_L,G4_MIN,G4_MAX,G4_DIFF,\
                            ,CPU0_F,CPU0_E,CPU0_D,CPU0_C,CPU0_B,CPU0_A,G1_MIN,G1_MAX,G1_DIFF,\
                            ,CPU0_G,CPU0_H,CPU0_I,CPU0_J,CPU0_K,CPU0_L,G2_MIN,G2_MAX,G2_DIFF \n")
        report_list.sort(key=lambda x: x['CMB'], reverse=True)
        for i in range(0, len(report_list)):
            cmb_num = report_list[i]['CMB']
            iteration = report_list[i]['value']['iteration'] 
            group1_dic = report_list[i]['value']['g1']
            group2_dic = report_list[i]['value']['g2']
            group3_dic = report_list[i]['value']['g3']
            group4_dic = report_list[i]['value']['g4']

            rf.write(str(cmb_num)+","+iteration+","+str(group3_dic['F'])+","+str(group3_dic['E'])+","+str(group3_dic['D'])+","+str(group3_dic['C'])+","+str(group3_dic['B'])+","+str(group3_dic['A'])+ \
                                ","+str(group3_dic['MIN'])+","+str(group3_dic['MAX'])+","+str(group3_dic['DIFF'])+","+ \
                                ","+str(group4_dic['G'])+","+str(group4_dic['H'])+","+str(group4_dic['I'])+","+str(group4_dic['J'])+","+str(group4_dic['K'])+","+str(group4_dic['L'])+ \
                                ","+str(group4_dic['MIN'])+","+str(group4_dic['MAX'])+","+str(group4_dic['DIFF'])+","+ \
                                ","+str(group1_dic['F'])+","+str(group1_dic['E'])+","+str(group1_dic['D'])+","+str(group1_dic['C'])+","+str(group1_dic['B'])+","+str(group1_dic['A'])+ \
                                ","+str(group1_dic['MIN'])+","+str(group1_dic['MAX'])+","+str(group1_dic['DIFF'])+","+ \
                                ","+str(group2_dic['G'])+","+str(group2_dic['H'])+","+str(group2_dic['I'])+","+str(group2_dic['J'])+","+str(group2_dic['K'])+","+str(group2_dic['L'])+ \
                                ","+str(group2_dic['MIN'])+","+str(group2_dic['MAX'])+","+str(group2_dic['DIFF'])+"\n")
        rf.close()
    


