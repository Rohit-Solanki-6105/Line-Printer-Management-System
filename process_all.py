import os
import glob
import datetime
import shutil
import json
from printer_manage import *

def print_students():
    with open('settings.settings', 'r') as settings_file:
        settings_data = json.load(settings_file)
                    # print(settings_data)
        kermit_path = settings_data['kermit_path']
    
    use_printer()
    os.chdir(kermit_path)
    os.system("print *.*")
    print(os.getcwd())
    print(os.listdir())
    for i in os.listdir():
        print(i)
        os.remove(i)
    # os.remove()
    release_printer()
    print(os.listdir())


def process_all_files_user(username, path):
    # Use glob.glob to collect files from the specified paths
    txt_files = glob.glob(os.path.join(path, "*.txt"))
    c_files = glob.glob(os.path.join(path, "*.c"))
    cpp_files = glob.glob(os.path.join(path, "*.cpp"))

    # Combine the lists of files
    all_files = txt_files + c_files + cpp_files

    for filename in all_files:
        username = filename.split('_')[0]
        username = username.rsplit('\\')[1]
        print(username)
        print(filename)
        process_file(filename, username)

    print_students()
    


def process_file(input_file, username):
    now = datetime.datetime.now()
    user = username
    if len(user) > 10:
        user = user[:10]

    with open(input_file, 'r') as infile, open("prt.var", 'w') as outfile:
        
        page_number = 1
        line_count = 0
        outfile.write(f"                                          DEPARTMENT OF COMPUTER SCIENCE                      Page = {page_number}\n")
        outfile.write(f"User = {user:<6}                                                                              Date = {now.day}\\{now.month}\\{now.year}\n")
        # outfile.write(f"-------------------------------------------------------------------------------------------------------------\n")

        tmp = infile.read(1)
        while tmp:
            if ord(tmp) < 0 or ord(tmp) > 127:
                print(f"Error in file {input_file}")
                return
            if tmp == '\n':
                line_count += 1
            if line_count >= 69:
                outfile.write('\n\n')
                page_number = page_number + 1
                outfile.write(f"                                           DEPARTMENT OF COMPUTER SCIENCE                        Page = {page_number}\n")
                outfile.write(f"User = {user:<6}                                                                              Date = {now.day}\\{now.month}\\{now.year}\n")
                # outfile.write(f"-------------------------------------------------------------------------------------------------------------\n")
                outfile.write('\n')
                line_count = 2 # because of above two lines
            if tmp == '\t':
                outfile.write("        ")
            else:
                outfile.write(tmp)
            tmp = infile.read(1)

    os.remove(input_file)
    # os.rename("prt.var", input_file)
    shutil.move("prt.var", input_file)
