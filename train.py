import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from features import extract_features

df = pd.read_csv("malicious_phish.csv")
df = df.sample(n=100000, random_state=42)
df["label"] = (df["type"] != "benign").astype(int)   # 1 = suspicious, 0 = safe

print("Extracting features...")
X = pd.DataFrame([extract_features(u) for u in df["url"]])
y = df["label"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Training model...")
model = RandomForestClassifier(n_estimators=100, max_depth=25,
                               random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print("Accuracy:", round(accuracy_score(y_test, pred), 4))
print(classification_report(y_test, pred, target_names=["safe", "suspicious"]))

joblib.dump({"model": model, "columns": list(X.columns)},
            "model.joblib", compress=3)
print("Saved model.joblib")