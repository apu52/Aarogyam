from flask import Flask, request, jsonify
import joblib  # Assuming you've saved the model using joblib

app = Flask(__name__)

# Load your model
model = joblib.load('your_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model.predict([data])  # Modify based on your model's input format
    return jsonify({'prediction': prediction[0]})
