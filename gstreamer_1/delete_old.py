#this script deletes the file,
#when the number of files in a designated folder excedes a given limit

# The oldest files in the folder are deleted first


import fnmatch
import os
import cv2

dir_path = '/home/pi/cctv/storage'
count = len(fnmatch.filter(os.listdir(dir_path), '*.avi')) #'*.*'
print('File Count:', count)

list_of_files = os.listdir(dir_path)
full_path = [str(dir_path)+"/{0}".format(x) for x in list_of_files]


"""print("list of files:")
print(list_of_files)
print("fullpath:")
print(full_path)"""

while(len(list_of_files) > 7):

    
    oldest_file = min(full_path, key=os.path.getctime)
    print(oldest_file)
    os.remove(os.path.abspath(oldest_file))
    list_of_files = os.listdir(dir_path)
    full_path = [str(dir_path)+"/{0}".format(x) for x in list_of_files]