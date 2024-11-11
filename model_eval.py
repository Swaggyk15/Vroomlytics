#Note, I decided to create a model_eval file to obtain the accuracy of the results of my predicted
#prices to see how well the model worked

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

#loaded in the cleaned dataset for the model
data = pd.read_csv('cleaned_used_cars.csv')
print("Cleaned dataset loaded in :) ")

#Similar to how I did in price_predictor.py, here I split the features into x
#and the price into y
X = data.drop(columns=['price'])
y = data['price']

#same as the price_predictor.py training splits:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#same as the price_predictor.py model:
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

#to compare the results of the actual datasets vs the predicted, the mode first had to make 
#predeictions on datasets that are actually within the csv file and then compare
#its prediction with what is really in the csv (hence, we get an accuracy score!)
y_pred = model.predict(X_test)

#calucations for mean absolute error, squared error, and r2 score
#For this portion I was unsure what exact statitsics I should have calculated and so I reffered
#to ai to help me with what statisctal analysis is necessary to dipslay:
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)


#to calculate the accuracy score, I had to first find the mean absolute percentage error (MAPE)
#using its formula:
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
#then I subrtacted the mape from 100 ot get an accuracy percetage so I could see how well my model worked
accuracy = 100 - mape

#displaying of results
print("\nFinal model evaluation metrics:")
print(f"Mean absolute error (MAE): {mae:.2f}")
print(f"Mean squared error (MSE): {mse:.2f}")
print(f"R² score: {r2:.2f}")
print(f"Mean absolute percentage Error (MAPE): {mape:.2f}%")
print(f"Model accuracy: {accuracy:.2f}%")

#lastly, I then saved the eval model as price_model_eval.pkl
import joblib
joblib.dump(model, 'price_model_eval.pkl')
print("\nModel saved as 'price_model_eval.pkl'")
