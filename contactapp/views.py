from django.shortcuts import render
from http.client import HTTPResponse
from .models import ContactUs
# ===================================

# import the required libraries 
import pickle 
import os.path 
from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request 
from googleapiclient.http import MediaFileUpload  
  
  
# Define the SCOPES. If modifying it, 
# delete the token.pickle file. 
SCOPES = ['https://www.googleapis.com/auth/drive'] 
# ====================================
from django.core.serializers.json import DjangoJSONEncoder
import json
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
# authorize the clientsheet 
client = gspread.authorize(creds)
print(client)
# ===================================

drive_creds = None 
if os.path.exists('token.pickle'): 
    with open('token.pickle', 'rb') as token: 
        drive_creds = pickle.load(token) 

if not drive_creds or not drive_creds.valid: 
    if drive_creds and drive_creds.expired and drive_creds.refresh_token: 
        drive_creds.refresh(Request()) 
    else: 
        flow = InstalledAppFlow.from_client_secrets_file( 
            'client_secret.json', SCOPES) 
        drive_creds = flow.run_local_server(port=0) 

    with open('token.pickle', 'wb') as token: 
        pickle.dump(drive_creds, token) 
        
service = build('drive', 'v3', credentials=drive_creds) 

def contact(request):
    
    thank = False
    file_names=''
    if request.method=="POST":
        try :
            first_name = request.POST.get('first_name','')
            last_name = request.POST.get('last_name','')
            email = request.POST.get('email','')
            mobile = request.POST.get('mobile','')
            message = request.POST.get('message','')
            attachments = request.FILES["attachments"]
            print(attachments)
            multiple_attachments = request.FILES.getlist('attachments','')
            print(multiple_attachments)
            contact = ContactUs(first_name=first_name, last_name=last_name, email=email, mobile=mobile, message=message)
            contact.save()
            thank = True
        
            file_names=str(contact.attachments)
            print(file_names)
            
            
            # # Google Sheet APT - Sheet Entry Updatation.==================
            wks = client.open('BOPBO').sheet1
            wks.append_row([contact.id,contact.first_name,contact.last_name,contact.email,contact.mobile,contact.message])
            print('-------')
            print(wks) 
            # ====================================
            # # Google Drive API- Attachments Updatation.==================

            
            folder_id = '1KAd7GfMwY2dFF0RyF94N4D-7ZL_lGPaB'
            source = './image.png'
            filename = multiple_attachments
            print(filename)
            for i in filename:
                print('******')
                file_name=str(i)
                print(file_name)
                file_metadata = {'name': file_name,'parents': [folder_id]}
                print(file_metadata)
                media = MediaFileUpload(source, mimetype='image/jpeg')
                print(media)
                file = service.files().create(body=file_metadata,
                                                    media_body=media,
                                                    fields='id').execute()
                print(file)  
            
          
                print('Upload Success!')

        except :
            print('File Upload Unsuccessfull')
        
    return render(request, 'contactus.html', {'thank': thank})
