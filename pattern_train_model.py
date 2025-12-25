# File: pattern_train_model.py
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# --- MODIFIED: Configuration filenames updated ---
TRAINING_DATA_CSV = "pattern_training_data.csv"
MODEL_FILE = "pattern_model.joblib"

# --- Main Training Logic (Essentially Unchanged) ---
if __name__ == "__main__":
    print("Starting model training process for Pattern Lock...")

    try:
        df = pd.read_csv(TRAINING_DATA_CSV)
    except FileNotFoundError:
        print(f"Error: Training data file '{TRAINING_DATA_CSV}' not found.")
        print("Please register some users first using the main application.")
        exit()

    if df['label'].nunique() < 2:
        print("Warning: Not enough unique users to train a robust model. At least 2 are needed.")
        print("Training will proceed for testing purposes if possible.")
        if len(df) < 5:
           exit()
    
    features = ['mean_hold_time', 'std_hold_time', 'mean_flight_time', 'std_flight_time', 'total_duration']
    X = df[features]
    y = df['label']

    # Stratify ensures that the test split has the same proportion of labels as the original dataset
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)



    print(f"Training data size: {len(X_train)}")
    print(f"Testing data size: {len(X_test)}")

    model = KNeighborsClassifier(n_neighbors=3)
    
    print("Training the KNN model...")
    model.fit(X_train, y_train)
    print("Model training complete.")

    if not X_test.empty:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\nModel Accuracy on test data: {accuracy * 100:.2f}%")

    print(f"Saving the trained model to '{MODEL_FILE}'...")
    joblib.dump(model, MODEL_FILE)
    print("✅ Model saved successfully!")