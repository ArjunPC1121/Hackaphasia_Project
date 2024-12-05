
# Load the dataset
def best_next_step(df):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn.ensemble import RandomForestClassifier


# Encoding categorical features
    label_encoders = {}
    for column in df.columns[:-1]:  # Exclude the target column
        if df[column].dtype == 'object':
            le = LabelEncoder()
            df[column] = le.fit_transform(df[column])
            label_encoders[column] = le

    # Splitting the dataset into features (X) and target (y)
    X = df.drop("Next_Step", axis=1)
    y = LabelEncoder().fit_transform(df["Next_Step"])  # Encode target labels

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

