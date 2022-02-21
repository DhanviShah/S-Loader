from multiprocessing import context
from venv import create
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
# import mysql.connector
from uploadFile.forms import FileForm

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import mysql.connector as sql

import os
import json



# Create your views here.

def handle_uploaded_file(f, flag_dup, flag_disp):
        if f.name.endswith('.csv') or f.name.endswith('.xls') or f.name.endswith('.xlsx'):
                
                # flag=False
                # perform the write operation into the folder (upload at server)
                with open('uploadFile/upload/' + f.name, 'wb+') as destination: 
                        for chunk in f.chunks():
                                destination.write(chunk)
                
                # after upload open the file depending on the extension
                if f.name.endswith('.csv'):
                        # update mysql database with csv
                        df = pd.read_csv('uploadFile/upload/' + f.name, header=[0])
                        # remove duplicates if two rows match
                        if flag_dup:
                                df = df.drop_duplicates()
                        
                        #data = df.values.tolist()
                        data = df.copy()
                        engine = create_engine('mysql+mysqldb://root:Searce123@localhost:3306/s_loader')
                        table_name = os.path.splitext(f.name)[0]
                        df.to_sql(name = table_name, con = engine, index = False)

                elif f.name.endswith('.xls') or f.name.endswith('.xlsx'):
                        df = pd.read_excel('uploadFile/upload/' + f.name, engine = 'openpyxl')
                        if flag_dup:
                                df = df.drop_duplicates()
                        
                        #data = df.values.tolist()
                        data = df.copy()
                        engine = create_engine('mysql+mysqldb://root:Searce123@localhost:3306/s_loader')
                        table_name = os.path.splitext(f.name)[0]
                        df.to_sql(name = table_name, con = engine, index_label= 'id')

                """"
                # add id attribute as primary key
                #m=sql.connect(host="localhost",user="root",password="Searce123",database="s_loader")
                cursor = m.cursor()
                query = "ALTER TABLE {} ADD COLUMN id INT PRIMARY KEY NOT NULL AUTO_INCREMENT FIRST".format(table_name)
                cursor.execute(query)
                m.commit()"""
                if flag_disp:
                        return data
                else :
                        return None

        else:
                print("not an excel file.")


def index(request):  
        data = None
        context = {}
        if request.POST:
                form = FileForm(request.POST, request.FILES)
                files = request.FILES.getlist('files')
                temp_dup = request.POST.get('drop_duplicates', False)
                temp_display = request.POST.get('display_file_content', False)

                if form.is_valid():
                        if len(files)>4:
                                context = {'msg' : 'You can only upload 4 files at max.'}
                                
                        else:
                                file_names = []
                                file_data = []
                                arr = []
                                for i,f in enumerate(files):
                                        file_cont = handle_uploaded_file(f, temp_dup, temp_display)
                                        #print(file_cont)
                                        file_names.append(f.name)
                                        # file_data.append(file_cont)
                                        if file_cont is not None:
                                                jason_records = file_cont.reset_index().to_json(orient = 'records')
                                                arr = []
                                                arr = json.loads(jason_records)
                                        #file_data.append(arr)

                                 
                                # context['file_cont'] = 
                                #data = pd.DataFrame(file_cont)
                                #print(file_cont)

                                #context['d'] = file_data 
                                context['d'] = arr 
                                context['msg'] = 'Following files successfully uploaded.'
                                context['names'] = file_names
                                        
        else :
                form = FileForm()
                context = {'msg' : 'Upload a file.'}

        context['form'] = form

        return render(request,"basic_form.html",context) 


def about(request):
    return render(request, 'about.html')

def datamonitor(request):
    return render(request, 'datamonitor.html')
       