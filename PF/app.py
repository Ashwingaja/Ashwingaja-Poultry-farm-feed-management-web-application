from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import io
import base64

# Load and prepare the data
data = pd.read_excel(r"C:\Users\bhava\Desktop\PF\poultrydata.xlsx")
data['Mortality Rate'] = data['MORT'] / data['BIRD COUNT']
X = data[['BIRD COUNT', 'FCR', 'AGE']]
y = data['DAILY']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)
"""
###
# prompt: # prompt: use multiple linear regression model use BIRD COUNT , FCR ,AGE to predict the sum of DAILY that are required at definite stage thus we can buy and store in warehouse

# ... (your existing imports and data loading)

# Prepare the data for multiple linear regression
X = data[['BIRD COUNT', 'FCR', 'AGE']]  # Features
y = data['DAILY']  # Target variable

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the multiple linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Function to predict daily feed for a given age range and other parameters
def predict_daily_feed(start_age, end_age, bird_count, fcr, step=1):
    predictions = {}
    for age in np.arange(start_age, end_age + step, step):
        user_input = np.array([[bird_count, fcr, age]])
        predicted_daily = model.predict(user_input)
        predictions[age] = predicted_daily[0]
    return predictions

# Get user input
while True:
    try:
        start_age = float(input("Enter the starting age: "))
        end_age = float(input("Enter the ending age: "))
        bird_count = float(input("Enter the bird count: "))
        fcr = float(input("Enter the feed conversion ratio (FCR): "))
        if start_age >= 0 and end_age >= start_age and bird_count > 0 and fcr > 0:
            break
        else:
            print("Invalid input. Please check your values.")
    except ValueError:
        print("Invalid input. Please enter numbers.")

# Predict daily feed for the specified range
predicted_daily_feed = predict_daily_feed(start_age, end_age, bird_count, fcr)

# Print or process predictions
for age, daily_feed in predicted_daily_feed.items():
    print(f"Predicted daily feed for age {age:.2f}: {daily_feed:.2f}")

# Calculate the total daily feed needed for the entire range
total_daily_feed = sum(predicted_daily_feed.values())
print(f"\nTotal daily feed needed for the age range {start_age} to {end_age}: {total_daily_feed:.2f}")
###"
"""

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        start_age = float(request.form['start_age'])
        end_age = float(request.form['end_age'])
        bird_count = float(request.form['bird_count'])
        fcr = float(request.form['fcr'])
        feed_cost_per_unit = float(request.form['feed_cost'])
        
        predictions = {}
        total_daily_feed = 0
        for age in np.arange(start_age, end_age + 1):
            user_input = np.array([[bird_count, fcr, age]])
            predicted_daily = max(0, model.predict(user_input)[0])
            predictions[age] = predicted_daily
            total_daily_feed += predicted_daily
        
        total_cost = total_daily_feed * feed_cost_per_unit
        
        return jsonify({"predictions": predictions, "total_cost": total_cost})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
