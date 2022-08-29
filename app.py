from fastapi import FastAPI
import uvicorn
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df=pd.read_csv("Car.csv")
df.head()

df.dropna(inplace=True)

df['mileage']=df['mileage'].str.split(' ').str[0]
df['mileage']=df['mileage'].astype(float)

df['engine']=df['engine'].str.split(' ').str[0]
df['engine']=df['engine'].astype(float)

fuel=pd.get_dummies(df['fuel'])
df=pd.concat([df.drop(['fuel'],axis=1),fuel],axis=1)

transmission=pd.get_dummies(df['transmission'])
df=pd.concat([df.drop(['transmission'],axis=1),transmission],axis=1)

seller=pd.get_dummies(df['seller_type'])
df=pd.concat([df.drop(['seller_type'],axis=1),seller],axis=1)

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
df['owner']=le.fit_transform(df['owner'])

df.head()

X=df[['km_driven','owner','mileage','engine','seats','Diesel','Petrol','CNG','Automatic','Manual']]

X.isnull().sum()

y=df['selling_price']

x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=23)


lr=LinearRegression()
lr.fit(x_train,y_train)

# Declaring our FastAPI instance
app = FastAPI()
 
# Defining path operation for root endpoint
@app.get('/')
def main():
    return {'message': 'Car Price prediction!'}

from pydantic import BaseModel
class request_body(BaseModel):
    Kilometers_driven : float
    Owner : float
    Mileage : float
    Engine_cc : float
    Seats : float
    Diesel : float
    Petrol : float
    CNG : float
    Automatic : float
    Manual : float

@app.post('/predict')
def predict(data : request_body):
    test_data = [[
            data.Kilometers_driven, 
            data.Owner, 
            data.Mileage, 
            data.Engine_cc,
            data.Seats,
            data.Diesel,
            data.Petrol,
            data.CNG,
            data.Automatic,
            data.Manual
    ]]
    Price = lr.predict(test_data)[0]
    return { 'Price' : Price}
