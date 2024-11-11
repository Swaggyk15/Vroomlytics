# Vroomlytics

Vroomlytics

What is it?
Vroomlytics is a car price prediction tool that I developed to help estimate the resale value of used cars based on various input features such as brand, model, year, mileage, fuel type, engine specifications, and more. The goal of this project is to assist users in determining a fair market price for used cars using data I gathered from the web and predictive modeling!

In all honesty, I developed this project on my own to gain hands-on experience with data preprocessing, machine learning model training, and developing a graphical user interface (GUI) using Python. Prior to this, I had only learned Python in my college courses and developed small personal projects. However, I wanted to take it to the next level and develop a useful tool that could potentially be used for predicting car resale prices!

Key features of my project:
- User-friendly GUI: Built with Tkinter, allowing users to input details such as car brand, model, mileage, engine specifications, and other attributes to predict the car's resale price.
- Data Preprocessing & Cleaning: Preprocessed data from a dataset of over 4,000 car listings to handle missing values, categorical encoding, and feature extraction.
- Machine Learning Model: Used a RandomForestRegressor model to predict car prices based on the input features.
- Model Evaluation: Developed a model evaluator using metrics such as Mean Absolute Error (MAE), Mean Squared Error (MSE), R² score, and Mean Absolute Percentage Error (MAPE) to assess accuracy.

What technologies did I use?
- Python: used as the main programming language that helped me with data processing, model training, and GUI development.
- Pandas & NumPy: Imported python libraries to assist in data manipulation, cleaning, and preprocessing.
- Scikit-Learn: Used for implementing the Random Forest Regression model and evaluating its performance.
- Joblib: For saving and loading the trained machine learning model.
- Tkinter: To build the (GUI) for easy user interaction.

What data did I use?
The entire data set I used can be seen and downloaded at: 
https://www.kaggle.com/datasets/taeefnajib/used-car-price-prediction-dataset/data

Why did I decide on using a Random Forest Regression model?
The Random Forest Regression model creates multiple decision trees and averages their predictions to improve accuracy and reduce overfitting. Given that my data could be converted to numerical (encoded) data, this model was a great fit for predicting the resale price of cars. The model was trained on 80% of the dataset and tested on the remaining 20%.

How accurate is my model?
The model I developed had the following results:
Mean absolute error (MAE): 19208.82
Mean squared error (MSE): 17468718136.28
R² score: 0.15
Mean absolute percentage Error (MAPE): 35.34%
Model accuracy: 64.66%

Note: These results show that the model performs reasonably well, but there’s still room for improvement!

How can you run this project yourself?
First make sure you have the latest version of python 3 isntalled and then do the following in the terminal (note I developed this using a mac and so instructions may vary):
# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

To run the gui simply do:
python gui.py

To obtain the results simply do:
python model_eval.py

Also make sure to check the requirements.txt file to see what latest version are required!

Notice: 
This project is far from perfect! But I really wanted to develop a machine learning model on my own so I could get experience with such tools and I am very happy with how it came out! Some future improvements could be to use a larger and more recent dataset to improve model accuracy, enhance the GUI to make it more intuitive and user-friendly, optimize the data preprocessing pipeline for better handling of missing values, and experiment with other machine learning models to see if accuracy can be improved!

Also know, that in this project I had the assitance of AI for some parts of my project! To ensure I have kept integrity and full tranparency, any code generated (as well as which parts I was assisted in) by AI has been commented to show that it has been generated, but all other code has been done by yours truly! 

Thank you for checking out my project!
- Kenny Monterroso 