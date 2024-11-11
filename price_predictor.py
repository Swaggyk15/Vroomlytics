import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

#After cleaning the used_cars.csv data and saving it to cleaned_used_cars.csv, I now had to load
#the data so I could use it for predicting the price and using the regression model.
data = pd.read_csv('cleaned_used_cars.csv')

#While testing, I kept running into an issue with the int_col still being saved into the cleaned data
#and so I decided to apply a second type of security featurity to ensure it would be dropped regardless
if 'int_col' in data.columns:
    data.drop('int_col', axis=1, inplace=True)

#x values had to be the features, and since there were several, I saved them into a list
features = ['brand', 'model', 'model_year', 'mileage', 'fuel_type', 'liters', 'cylinders', 
            'transmission', 'accident', 'clean_title']
X = data[features]

#the y value = what we are trying to solve for, and so in this case it was the predicted price
y = data['price']

#training and testing was split, but focus was more on training compared to testing
#Note for the future: I could have improved my results by trying out different balances of
#splits, but for this project I decdided to go with 20% testing and 80% training. Definitely
#something to think about!
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#first needed to initialize the random forest regressor:
#n_estimators: I tested my model with n = 100, 200, 300, ... 1000 for imporoved accuracy, but realized
#due to the small data set I am working with, past 200 yielded not much imporved and so for the sake
#of saving cpu usage and keeping accuracy, I decided on 200.
#accuracy as more trees developed = better accuracy, but I also had to esnure that it didn't
#take up too much cpu power that way any user can use the program with no cpu complications.
#random_state: I resulted to advice via stack overflow, in which 42 is commonly used 
#as the random_state, but the importance was to esnure 42 was used in both the initialization of
#the model and when we split the training/testing
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

#saved the final random forest regression model to price_model.pkl
joblib.dump(model, 'price_model.pkl')
print("Random forest regression model saved to 'price_model.pkl' :)")
