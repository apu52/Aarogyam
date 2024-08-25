import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

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

# Save the model, scaler, and encoders as pickle files
with open('gradient_boosting_model.pkl', 'wb') as model_file:
    pickle.dump(model_gbm, model_file)

with open('scaler.pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)

with open('label_encoders.pkl', 'wb') as encoder_file:
    pickle.dump(label_encoders, encoder_file)

with open('target_encoder.pkl', 'wb') as target_encoder_file:
    pickle.dump(target_encoder, target_encoder_file)

print("Model and preprocessors saved as pickle files.")
