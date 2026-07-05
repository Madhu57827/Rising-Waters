import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

# ==========================
# LOAD DATASET
# ==========================

DATASET = "dataset.xlsx"

df = pd.read_excel(DATASET)

print("Dataset Loaded Successfully")
print(df.head())

# ==========================
# HANDLE MISSING VALUES
# ==========================

df = df.dropna()

# ==========================
# SELECT FEATURES
# ==========================

feature_columns = [
    "Temp",
    "Humidity",
    "Cloud Cover",
    "ANNUAL",
    "Jan-Feb",
    "Mar-May",
    "Jun-Sep",
    "Oct-Dec",
    "avgjune",
    "sub"
]

X = df[feature_columns]
y = df["flood"]

# ==========================
# TRAIN TEST SPLIT
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ==========================
# STANDARD SCALER
# ==========================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==========================
# MODEL
# ==========================

model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    random_state=42,
    eval_metric="logloss"
)

model.fit(X_train_scaled, y_train)

# ==========================
# EVALUATION
# ==========================

pred = model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, pred)

print(f"\nAccuracy : {accuracy * 100:.2f}%")
print(classification_report(y_test, pred))

# ==========================
# SAVE MODEL
# ==========================

joblib.dump(model, "floods.save")
joblib.dump(scaler, "transform.save")

print("\nModel Saved Successfully")
print("floods.save")
print("transform.save")
