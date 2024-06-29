import os
import glob

course = "mcs2"
subject = "DBMS"

def fetch_Student(course, subject):
    directory_path = 'Z:\\' 
    path = glob.glob(os.path.join(directory_path, course + '*',"print",subject))
    print(path)

fetch_Student(course, subject)

