from django.shortcuts import render, HttpResponse
import os
from django.conf import settings
import pickle as pk
import pandas as pd 

pipe_path = os.path.join(settings.BASE_DIR, 'static', 'model', 'pipe.pickle')
data_path = os.path.join(settings.BASE_DIR, 'static', 'model', 'df.pickle')

with open(pipe_path, "rb") as pipe_file:
    pipe = pk.load(pipe_file)
    print(pipe)

with open(data_path, "rb") as data_file:
    data = pk.load(data_file)
    print(data)

def insert(request):
    return render(request, "input.html", {"dropDownData" : dropDownData})

dropDownData={
    "gender" : data['gender'].unique(),
    "age" : range(0,80),
    "hypertension" : data['hypertension'].unique(),
    "heart_disease" : data['heart_disease'].unique(),
    "smoking_history" : data['smoking_history'].unique(),
    "bmilevel" : range(0,100),
    "HbA1c_level" : range(1,10),
    "bsl" : range(60,300)
    }

def data(request):
    print("helo")
    if request.method == "GET":
        gender = request.GET.get('gender')
        age = request.GET.get('age')
        hypertension = request.GET.get('hypertension')
        heart_disease = request.GET.get('heart_disease')
        smoking_history = request.GET.get('smoking_history')
        bmilevel = request.GET.get('bmilevel')
        HbA1c_level = request.GET.get('HbA1c_level')
        bsl = request.GET.get('bsl')
        print(gender, age, hypertension, heart_disease, smoking_history, bmilevel, HbA1c_level, bsl)

        if (gender and age and hypertension and heart_disease and smoking_history and 
            bmilevel and HbA1c_level and bsl):

            data_for_predict = pd.DataFrame([[gender, age, hypertension, heart_disease, smoking_history, 
                                           bmilevel, HbA1c_level, bsl]],
                                         columns=['gender', 'age', 'hypertension', 'heart_disease', 
                                                  'smoking_history', 'BMI_Level', 'HbA1c_level', 'blood_glucose_level'])
            print(data_for_predict)
            predict_value = pipe.predict(data_for_predict)
            print(predict_value)
            return render(request, "input.html", {"predict_value" : predict_value, "dropDownData" : dropDownData})
        
        else:
            return render(request, "input.html", {"dropDownData" : dropDownData})
        
    return render("/")

