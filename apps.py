import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import requests
import json


models = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)


@app.route('/',methods=['GET'])
def home():
    return "hello world"

@app.route('/predict',methods=['POST'])


def predict():
    
    temp_array = list()
    my_prediction=0

    obj = {'staff_id':request.json['staff_id']}
    resp=requests.post('https://limitless-shelf-60565.herokuapp.com/api/student/staff/getscore',obj)
    jsonData = json.loads(resp._content)
    for i in range(len(jsonData['data'])):
      if jsonData:
          
          stu = 1
          if((jsonData['data'][i]['s1'] and jsonData['data'][i]['s2'] and jsonData['data'][i]['s3'] and jsonData['data'][i]['s4'])=='0.00'):
              return 0
          else:
              mrk1 = jsonData['data'][i]['s1']
              mrk2 = jsonData['data'][i]['s2']
              mrk3 = jsonData['data'][i]['s3']
              mrk4 = jsonData['data'][i]['s4'] 
            
          if(jsonData['data'][i]['s5']=='0.00'):
              mrk1 = jsonData['data'][i]['s1']
              mrk2 = jsonData['data'][i]['s2']
              mrk3 = jsonData['data'][i]['s3']
              mrk4 = jsonData['data'][i]['s4']
          
          elif(jsonData['data'][i]['s6']=='0.00'):
              mrk1 = jsonData['data'][i]['s5']
            
          elif(jsonData['data'][i]['s7']=='0.00'):
              mrk2 = jsonData['data'][i]['s6']
              mrk1 = jsonData['data'][i]['s5']
              
          else:
              mrk3 = jsonData['data'][i]['s7']
              mrk2 = jsonData['data'][i]['s6']
              mrk1 = jsonData['data'][i]['s5']
              
      
          temp_array = temp_array + [stu,mrk1,mrk2,mrk3,mrk4]
          print(temp_array)
          data = np.array([temp_array])
          my_prediction = float(models.predict(data)[0])
    
    upload_Prediction=requests.post('https://limitless-shelf-60565.herokuapp.com/api/student/staff/predict',{'register_no':jsonData['data'][i]['register_no'],'prediction':my_prediction})
    return json.loads(upload_Prediction._content)['Message']

            


if __name__ == '__main__':
  app.run(debug=True)
