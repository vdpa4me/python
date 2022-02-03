import sys
import os


# empty list
sentence_list = []
skip_list = ['WEBVTT','STYLE','::cue()','}','font-family','text-shadow','-->','<i>']
new_file_name = ''

if __name__ == '__main__':

    # get current directory 
    dir_name = os.path.dirname(os.path.realpath(__file__))

    # get failes in the current directory 
    file_list = []
    for (root, directories, files) in os.walk(dir_name):
        for file in files:
            file_path = os.path.join(root, file)
            path,ext = os.path.splitext(file_path)
            if ext in '.vtt' :
                file_list.append(file_path)
    # list sort 
    file_list.sort()

    # new file for writing
    new_file_name = input("Enter file name : ")
    new_file_name = new_file_name + ".txt"
    new_file_name = os.path.join(dir_name, new_file_name)
    print(new_file_name)

    # result_path = the current directory 
    result_path = dir_name
    
    print('START LOG PARSING ... ')

    for fname in file_list:
        print(fname)
        section = fname + '\n'
        sentence_list.append(section)
        logfile = open(fname, 'rb')
        current_line = logfile.readline().decode('utf-8')
        while current_line:
            # Skip empty line
            if current_line == '\n':
                current_line = logfile.readline().decode('utf-8')
                continue
            # skip functional line
            elif any(x in current_line for x in skip_list):
                current_line = logfile.readline().decode('utf-8')
                continue
            else:
                sentence_list.append(current_line)
            current_line = logfile.readline().decode('utf-8')
        logfile.close()
        #user_input = input("Keep going?")
        #if user_input != 'yes':
        #    print(sentence_list)
        #    sys.exit(1)
    
    # write a file 
    newFile = open(new_file_name, 'w', encoding='utf-8')
    for sentense in sentence_list:
        newFile.write(sentense)
    newFile.close()


