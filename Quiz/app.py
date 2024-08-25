from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the model, scaler, and encoders
model = pickle.load(open('gradient_boosting_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
label_encoders = pickle.load(open('label_encoders.pkl', 'rb'))
target_encoder = pickle.load(open('target_encoder.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('quiz.html', result='')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract and convert form data
        user_input = {
            'Age': int(request.form['Age']),
            'Marital_Status': request.form['Marital_Status'],
            'Education_Level': request.form['Education_Level'],
            'Number_of_Children': int(request.form['Number_of_Children']),
            'Smoking_Status': request.form['Smoking_Status'],
            'Physical_Activity_Level': request.form['Physical_Activity_Level'],
            'Employment_Status': request.form['Employment_Status'],
            'Income': float(request.form['Income']),
            'Alcohol_Consumption': request.form['Alcohol_Consumption'],
            'Dietary_Habits': request.form['Dietary_Habits'],
            'Sleep_Patterns': request.form['Sleep_Patterns'],
            'History_of_Substance_Abuse': request.form['History_of_Substance_Abuse'],
            'Family_History_of_Depression': request.form['Family_History_of_Depression'],
            'Chronic_Medical_Conditions': request.form['Chronic_Medical_Conditions']
        }

        # Debug: Print the raw input
        print("Raw user input:", user_input)

        # Handle unseen labels
        for column in user_input:
            if column in label_encoders:
                try:
                    user_input[column] = label_encoders[column].transform([user_input[column]])[0]
                except ValueError:
                    user_input[column] = -1  # Assign a default value for unseen labels

        # Convert the user input to DataFrame
        input_df = pd.DataFrame([user_input])

        # Debug: Print the DataFrame
        print("Input DataFrame:", input_df)

        # Standardize column names to match training data
        input_df.columns = input_df.columns.str.replace(' ', '_')

        # Scale the input
        input_scaled = scaler.transform(input_df)

        # Debug: Print the scaled input
        print("Scaled Input:", input_scaled)

        # Make prediction
        raw_result = model.predict(input_scaled)[0]
        print(f"Raw model prediction: {raw_result}")

        result = target_encoder.inverse_transform([raw_result])[0]

        # Interpret the result
        if result == 'Yes':  # Assuming 'No' means not likely depressed
            prediction_text = "You are not likely to have a history of mental illness."
        else:
            prediction_text = "You are likely to have a history of mental illness."

        print(f"Final result: {prediction_text}")

    except Exception as e:
        prediction_text = f"An error occurred: {e}"
        print(f"Error: {e}")

    return render_template('quiz.html', result=prediction_text)


if __name__ == '__main__':
    app.run(debug=True)
