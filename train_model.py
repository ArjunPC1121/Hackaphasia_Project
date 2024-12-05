import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load your dataset
df = pd.read_csv("Expanded_Career_Counselling.csv")

# Encode categorical features
label_encoders = {}
for column in df.columns[:-1]:  # Exclude the target column
    if df[column].dtype == 'object':
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

# Encode the target column (Next_Step)
target_encoder = LabelEncoder()
df["Next_Step"] = target_encoder.fit_transform(df["Next_Step"])

# Split the dataset into features (X) and target (y)
X = df.drop("Next_Step", axis=1)
y = df["Next_Step"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save the trained model and encoders
joblib.dump(model, "career_counseling_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")
joblib.dump(target_encoder, "target_encoder.pkl")
