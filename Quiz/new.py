import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the Excel file
file_path = 'depression.xlsx'
data = pd.read_excel(file_path)

data.columns = data.columns.str.replace(' ', '_')

# Proceed with the rest of your code
target = 'History_of_Mental_Illness'

# Dropping the Name column and target from features
X = data.drop(columns=['Name', target])
y = data[target]

# Encoding categorical variables
label_encoders = {}
for column in X.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    X[column] = le.fit_transform(X[column])
    label_encoders[column] = le

# Encoding target variable
target_encoder = LabelEncoder()
y = target_encoder.fit_transform(y)

# Scaling the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Applying SMOTE to handle class imbalance
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

# Splitting the resampled data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Training the Gradient Boosting model
model_gbm = GradientBoostingClassifier(random_state=42)
model_gbm.fit(X_train, y_train)

# Evaluate the model accuracy
y_pred = model_gbm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.2%}")

# Print the classification report
report = classification_report(y_test, y_pred, target_names=target_encoder.classes_)
print("\nClassification Report:\n", report)

# Feature importance analysis
feature_importances = pd.Series(model_gbm.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nFeature Importances:\n", feature_importances)

# Function to take user input and predict mental illness
def predict_depression():
    user_data = {}

    # Collect input for each feature
    for column in X.columns:
        try:
            if X[column].dtype == 'int64' or X[column].dtype == 'float64':
                user_data[column] = float(input(f"Enter your {column}: "))
            else:
                print(f"Possible values for {column}: {list(label_encoders[column].classes_)}")
                user_input = input(f"Enter your {column}: ")
                # Ensure the input is valid
                if user_input not in label_encoders[column].classes_:
                    print(f"Invalid input. Please choose from {list(label_encoders[column].classes_)}.")
                    return
                user_data[column] = label_encoders[column].transform([user_input])[0]
        except ValueError:
            print(f"Invalid input for {column}. Please enter a valid number or categorical value.")
            return

    # Convert the user data to a DataFrame
    user_df = pd.DataFrame([user_data])

    # Ensure the DataFrame has the same columns as X
    user_df = user_df.reindex(columns=X.columns, fill_value=0)

    # Scale the user data
    user_scaled = scaler.transform(user_df)

    # Make a prediction
    prediction = model_gbm.predict(user_scaled)
    prediction_label = target_encoder.inverse_transform(prediction)[0]

    # Output the result
    if prediction_label == 'Yes':
        print("\nPrediction: You are likely to have a history of mental illness.")
    else:
        print("\nPrediction: You are not likely to have a history of mental illness.")

# Run the prediction function
predict_depression()
