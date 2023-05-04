#this script deletes the file, AND UPLOADS  the file to cloud
#when the number of files in a designated folder excedes a given limit(here it would be set to 2)
# The oldest files in the folder are uploaded to GCP and then deleted 
# for security puropse i.e to restrict the upload acess a  "sevice-account-key.json" is
#created in GCP and used here for authentication

#The files which are recorded by default comes with a diffrent name,they are renamed on the fly as
#they are being uploaded on to cloud


import fnmatch
import os
import cv2
from google.cloud import storage

dir_path = '/home/pi/cctv/storage3'
count = len(fnmatch.filter(os.listdir(dir_path), '*.avi')) #'*.*'
# Set the path to the service account key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/pi/cctv/service_account_gcp.json'
# Create a Google Cloud Storage client
client = storage.Client()
# Set the name of the bucket you want to upload to
bucket_name = 'first_surveyaan_cctv'
# Get a reference to the bucket
bucket = client.bucket(bucket_name)

#print('File Count:', count)
number=0
#we'll be using an infinate loop as our script runs as long as camera is recording
while True:
    
    list_of_files = os.listdir(dir_path)
    full_path = [str(dir_path)+"/{0}".format(x) for x in list_of_files]

    while(len(list_of_files) > 1):

        
        oldest_file = min(full_path, key=os.path.getctime) #oldest file is localted
        print(oldest_file)
        
        # Set the path to the file you want to upload
        file_path = str(os.path.abspath(oldest_file))
        #renaming the file
        new_file_name = str(number)
        number=number+1
        number=number%24
        
        blob = bucket.blob(new_file_name)
        blob.upload_from_filename(file_path)
        
        #waiting for uploading to finish
        while not blob.exists():
            continue
        print('uploaded {}'.format((number - 1)%24))
        #deleting the uploaded video file
            
        os.remove(os.path.abspath(oldest_file))
        list_of_files = os.listdir(dir_path)
        full_path = [str(dir_path)+"/{0}".format(x) for x in list_of_files]
