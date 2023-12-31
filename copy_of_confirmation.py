# -*- coding: utf-8 -*-
"""Copy of Confirmation

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a6POdtZRh3TLEiDR371lNi2ALJ77Q9lM
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
from scipy.stats import chi2_contingency

# Data transformation
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Deep Learning Model
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from google.colab import drive
drive.mount('/content/drive')

#Read data with error handling for encoding issues
try:
    data = pd.read_csv("/content/drive/MyDrive/Thesis project/MY2023 Fuel Consumption Ratings.csv", encoding='utf-8')
except UnicodeDecodeError:
    data = pd.read_csv("/content/drive/MyDrive/Thesis project/MY2023 Fuel Consumption Ratings.csv", encoding='latin1')
data

data.info()

data.columns

data[['CO2 Rating','Smog Rating','CO2 Emissions (g/km)']].corr()

df= data.drop(['Model Year','Make','Model','Fuel Consumption City (L/100km)','Fuel Consumption Hwy (L/100km)','Fuel Consumption Comb (mpg)','CO2 Emissions (g/km)','Smog Rating'],axis=1)
df

df = df.rename(columns = {'Vehicle Class':'Vehicle Class', 'Engine Size(L)':'Engine Size', 'Cylinders': 'Cylinders', 'Transmission':'Transmission','Fuel Type':'Fuel Type', 'Fuel Consumption Comb (L/100km)':'Fuel Consumption', 'CO2 Rating':'CO2 Rating'})

df.isna().sum()

df['Fuel Type'].fillna((df['Fuel Type'].mode()[0]), inplace=True)
df.head()

df['CO2 Rating'].fillna(0,inplace=True)
new_ratting = []

for fuel,co2 in zip(df['Fuel Consumption'], df['CO2 Rating']):
    if co2==0:
        if 20 <= fuel:
            new_ratting.append(1)
        elif 16.0 <= fuel < 20.0:
            new_ratting.append(2)
        elif 14.0 <= fuel < 16.0:
            new_ratting.append(3)
        elif 12.0 <= fuel < 14.0:
            new_ratting.append(4)
        elif 10.0 <= fuel < 12.0:
            new_ratting.append(5)
        elif 8.0 <= fuel < 10.0:
            new_ratting.append(6)
        elif 7.0 <= fuel < 8.0:
            new_ratting.append(7)
        elif 6.0 <= fuel < 7.0:
            new_ratting.append(8)
        elif 5.0 <= fuel < 6.0:
            new_ratting.append(9)
        elif fuel < 5.0:
            new_ratting.append(10)
    else:
        new_ratting.append(co2)


df['CO2 Rating'] = new_ratting
df.isna().sum()

df.corr()

df.corr()["Fuel Consumption"].to_frame()

for i in df.columns:
    print(i)
    print(df[i].unique(),'\n')

df = df.replace({'Transmission' : {'AM8':'AM', 'AS10': 'AS', 'A8':'A', 'A9':'A', 'AM7':'AM', 'AM9':'AM', 'AS8':'AS', 'M6':'M', 'AS6':'AS', 'AS9':'AS', 'A10':'A', 'A6':'A', 'M5':'M', 'M7':'M', 'AV7':'AV', 'AV1':'AV', 'AM6':'AM', 'AS7':'AS', 'AV8':'AV', 'AV6':'AV', 'AV10':'AV', 'AS5':'AS', 'A7':'A'}})
df

df['Transmission'].unique()

df[['Engine Size (L)','Cylinders','Fuel Consumption','CO2 Rating']].describe()

plt.figure(figsize=(13,6), dpi=150)
chart1=sns.histplot(data=df, x='Transmission', color='DarkOliveGreen')
chart1.bar_label(chart1.containers[0],size=10)
plt.show()

plt.figure(figsize=(5,4), dpi=150)
chart1=sns.histplot(data=df, x='Fuel Type', color='PaleVioletRed')
chart1.bar_label(chart1.containers[0],size=10)
plt.show()

column_set = ['Cylinders','Engine Size (L)','CO2 Rating','Fuel Consumption']
color_set = ['pink','brown','Thistle', 'SaddleBrown']
for colors,col in zip(color_set,column_set):
    plt.figure(figsize=(13,6), dpi=150)
    chart1=sns.histplot(data=df, x=col, color=colors)
    chart1.bar_label(chart1.containers[0],size=12)
    plt.show()

plt.figure(figsize=(13,6), dpi=150)
sns.pairplot(df, hue='Fuel Type',diag_kind='hist')

plt.figure(figsize=(13,6), dpi=150)
plt.xticks(rotation=45)
plt.title('Cylinders vs Consumption',size=20)
chart1=sns.barplot( data=df, x="Cylinders", y="Fuel Consumption",palette='mako_r', ci=None)
plt.xlabel('Cylinders',size=20)
plt.ylabel('Fuel Consumption',size=20)
chart1.bar_label(chart1.containers[0],size=12)
plt.show()

plt.figure(figsize=(13,6), dpi=150)
sns.heatmap(df.corr(),annot=True)

# from scipy.stats import chi2_contingency
fuel_type= pd.crosstab(df['Transmission'],df['Fuel Type'])
fuel_type

Chi_square_statistic,p,dof,expec = chi2_contingency(fuel_type)
alpha = 0.05
print("p_value is " + str(p))
if p <= alpha:
    print('Dependent')
    print('dof is ' +str(dof))
else:
    print('Independent')
    print('dof is ' +str(dof))

Class=pd.crosstab(df['Transmission'],df['Vehicle Class'])
Class

Chi_square_statistic,p,dof,expec = chi2_contingency(Class)
alpha = 0.05
print("p_value is " + str(p))
if p <= alpha:
    print('Dependent')
    print('dof is ' +str(dof))
else:
    print('Independent')
    print('dof is ' +str(dof))

for col in df.columns:
    if df[col].dtypes!= object:
        sns.boxplot(y=col,data=df)
        plt.show()

for col in df.columns:
    if df[col].dtypes!= object:
        percentile_25=df[col].quantile(0.25)
        percentile_75=df[col].quantile(0.75)
        IQR=percentile_75-percentile_25
        upper_limit=percentile_75+(1.5*IQR)
        lower_limit=percentile_25-(1.5*IQR)
        df=df[df[col]<=upper_limit]
        df=df[df[col]>=lower_limit]
        plt.figure()
        sns.boxplot(y=col,data=df)

df.shape

# from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

order = ['AV', 'AM', 'M', 'AS', 'A']

od = OrdinalEncoder(categories = [order])

df["Transmission_X"] = od.fit_transform(df[["Transmission"]])

order = ['Two-seater','Minicompact','Compact','Subcompact','Mid-size','Full-size','SUV: Small','SUV: Standard','Minivan',\
         'Station wagon: Small','Station wagon: Mid-size', 'Pickup truck: Small', 'Special purpose vehicle',\
         'Pickup truck: Standard']

od = OrdinalEncoder(categories = [order])

df["Vehicle Class_X"] = od.fit_transform(df[["Vehicle Class"]])
df.head(10)

new_df = df['Fuel Type'].str.get_dummies()
new_df

df= pd.concat([df,new_df], axis =1)
df.head()

# Data preprocessing

x = df.drop(["Fuel Type", 'Fuel Consumption', "Vehicle Class", "Transmission"], axis=1)
y = df['Fuel Consumption']
x.head()

y.head().to_frame()

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Split the data into training, validation, and test sets
# Adjust the test_size and validation_size ratios as needed
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.1, random_state=42)

# Standardize the data
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_val = sc.transform(x_val)
x_test = sc.transform(x_test)
x_train

x_test

x_val

from keras.models import Sequential
from keras.layers import Dense
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# Define and train the deep learning model with more hidden layers
dl_model = Sequential()
dl_model.add(Dense(256, input_dim=x_train.shape[1], activation='relu'))
dl_model.add(Dense(256, activation='relu'))  # Adding a hidden layer with 256 neurons
dl_model.add(Dense(256, activation='relu'))  # Adding another hidden layer with 256 neurons
dl_model.add(Dense(256, activation='relu'))  # Adding one more hidden layer with 256 neurons
dl_model.add(Dense(256, activation='relu'))  # Adding another hidden layer with 256 neurons
dl_model.add(Dense(1, activation='linear'))  # Output layer for regression

dl_model.compile(loss='mean_squared_error', optimizer='adam')
history = dl_model.fit(x_train, y_train, epochs=100, batch_size=32, validation_data=(x_val, y_val))

# After training, you can evaluate the model on a test dataset
y_pred = dl_model.predict(x_test)  # Make predictions on the test data

# Calculate evaluation metrics
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print the evaluation metrics
print(f"Mean Squared Error (MSE): {mse}")
print(f"Mean Absolute Error (MAE): {mae}")
print(f"R-squared (R2) Score: {r2}")

# Plot training & validation loss values
plt.figure(figsize=(12, 9))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Make predictions using the DL model
dl_predictions = dl_model.predict(x_test)

# Combine DL predictions with the original features
x_test_with_dl_predictions = np.hstack((x_test, dl_predictions))

# Create an enhanced SVM model
svm_model = SVR(kernel='rbf', C=10, gamma=0.1)  # Customize kernel and hyperparameters

svm_model.fit(x_test_with_dl_predictions, y_test)

# Make predictions with the enhanced SVM model
svm_predictions = svm_model.predict(x_test_with_dl_predictions)

# Evaluate the enhanced model
mse_svm = mean_squared_error(y_test, svm_predictions)
mae_svm = mean_absolute_error(y_test, svm_predictions)
r2_svm = r2_score(y_test, svm_predictions)

# Print evaluation metrics
print(f"Enhanced Model Test MSE: {mse_svm}")
print(f"Enhanced Model Test MAE: {mae_svm}")
print(f"Enhanced Model Test R-squared (R2) Score: {r2_svm}")

# Compare predicted and actual values
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))

# Plot the actual values as a straight line
plt.plot(y_test, y_test, color='red', linestyle='--', linewidth=2, label="Actual Values (Straight Line)")

# Scatter plot for predicted values
plt.scatter(y_test, svm_predictions, alpha=0.5, label="Predicted Values (Dots)")
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Actual vs. Predicted Values (Stacked Model)")
plt.legend()
plt.show()

# Make predictions with the enhanced SVM model
svm_predictions = svm_model.predict(x_test_with_dl_predictions)

# Calculate the percent difference between predicted and actual values
percent_difference = ((svm_predictions - y_test) / y_test) * 100

# Create a DataFrame to display the results
results_df = pd.DataFrame({'Actual Values': y_test, 'Predicted Values': svm_predictions, 'Percent Difference (%)': percent_difference})

# Save the Random Forest model using joblib
joblib.dump(svm_model, 'svm_model.pkl')

# Print the DataFrame
print(results_df)

import pickle as pk
filename = "scaled_data.pkl"
pk.dump(sc, open(filename, "wb")) #write binary = wb
loaded_scaler = pk.load(open("scaled_data.pkl", "rb")) #read binary = rb
filename = "svm_model.pkl"
pk.dump(dl_model, open(filename, "wb"))
loaded_model = pk.load(open("svm_model.pkl", "rb"))

inp = ["SUV: Small",3.0,7,"AS",5.0,"X"]    # input example

def input_converter(inp):
    vcl = ['Two-seater', 'Minicompact', 'Compact', 'Subcompact', 'Mid-size', 'Full-size', 'SUV: Small', 'SUV: Standard', 'Minivan',
           'Station wagon: Small', 'Station wagon: Mid-size', 'Pickup truck: Small', 'Special purpose vehicle', 'Pickup truck: Standard']
    trans = ['AV', 'AM', 'M', 'AS', 'A']
    fuel = ["D", "E", "X", "Z"]
    lst = []
    for i in range(9):
        if type(inp[i]) == str:
            if inp[i] in vcl:
                lst.append(vcl.index(inp[i]))
            elif inp[i] in trans:
                lst.append(trans.index(inp[i]))
            elif inp[i] in fuel:
                if fuel.index(inp[i]) == 0:
                    lst.extend([1, 0, 0, 0])
                    break
                elif fuel.index(inp[i]) == 1:
                    lst.extend([0, 1, 0, 0])
                    break
                elif fuel.index(inp[i]) == 2:
                    lst.extend([0, 0, 1, 0])
                    break
                elif fuel.index(inp[i]) == 3:
                    lst.extend([0, 0, 0, 1])
        else:
            lst.append(inp[i])

    arr = np.asarray(lst)
    arr = arr.reshape(1, -1)
    arr = loaded_scaler.transform(arr)
    prediction = loaded_model.predict(arr)

    return f"The Fuel Consumption L/100km is {round(prediction[0][0], 2)}"



input_converter(inp)