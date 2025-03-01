from django.shortcuts import render, HttpResponse
import os
from django.conf import settings
import pickle as pk
import pandas as pd
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Diabetes_Check_Application.settings')
django.setup()

# Define paths for the model and data files
pipe_path = os.path.join(settings.BASE_DIR, 'static', 'model', 'pipe.pickle')
data_path = os.path.join(settings.BASE_DIR, 'static', 'model', 'df.pickle')

# Load the model pipeline
try:
    with open(pipe_path, "rb") as pipe_file:
        pipe = pk.load(pipe_file)
        print(pipe)
except Exception as e:
    print(f"Error loading pipeline: {e}")

# Load the data
try:
    with open(data_path, "rb") as data_file:
        data = pk.load(data_file)
        print(data)
except Exception as e:
    print(f"Error loading data: {e}")

# Define the dropdown data for the input form
dropDownData = {
    "gender": data['gender'].unique(),
    "age": range(0, 80),
    "hypertension": data['hypertension'].unique(),
    "heart_disease": data['heart_disease'].unique(),
    "smoking_history": data['smoking_history'].unique(),
    "bmilevel": range(0, 100),
    "HbA1c_level": range(1, 10),
    "bsl": range(60, 300)
}

# Render the input form
def insert(request):
    return render(request, "input.html", {"dropDownData": dropDownData})

# Handle the form submission and make predictions
def data(request):
    if request.method == "GET":
        # Get form data
        gender = request.GET.get('gender')
        age = request.GET.get('age')
        hypertension = request.GET.get('hypertension')
        heart_disease = request.GET.get('heart_disease')
        smoking_history = request.GET.get('smoking_history')
        bmilevel = request.GET.get('bmilevel')
        HbA1c_level = request.GET.get('HbA1c_level')
        bsl = request.GET.get('bsl')
        print(gender, age, hypertension, heart_disease, smoking_history, bmilevel, HbA1c_level, bsl)

        # Check if all fields are filled
        if (gender and age and hypertension and heart_disease and smoking_history and 
            bmilevel and HbA1c_level and bsl):

            # Prepare data for prediction
            data_for_predict = pd.DataFrame([[gender, age, hypertension, heart_disease, smoking_history, 
                                            bmilevel, HbA1c_level, bsl]],
                                            columns=['gender', 'age', 'hypertension', 'heart_disease', 
                                                'smoking_history', 'BMI_Level', 'HbA1c_level', 'blood_glucose_level'])
            print(data_for_predict)
            
            # Make prediction
            try:
                predict_value = pipe.predict(data_for_predict)
                print(predict_value)
            except Exception as e:
                print(f"Error making prediction: {e}")
                predict_value = ["Error making prediction"]
            
            # Render the result
            return render(request, "input.html", {"predict_value": predict_value, "dropDownData": dropDownData})
        
        else:
            # Render the form again if not all fields are filled
            return render(request, "input.html", {"dropDownData": dropDownData})
        
    return render("/")

