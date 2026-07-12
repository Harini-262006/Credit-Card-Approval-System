import pandas as pd
import numpy as np
import pickle
import os

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score


# ----------------------------
# Load datasets
# ----------------------------

app = pd.read_csv("dataset/application_record.csv")
credit = pd.read_csv("dataset/credit_record.csv")


# ----------------------------
# Merge datasets
# ----------------------------

data = app.merge(credit, on="ID")


# ----------------------------
# Create Target Variable
# ----------------------------

bad_status = ['2','3','4','5']

data['STATUS'] = data['STATUS'].astype(str)

data['TARGET'] = data['STATUS'].apply(
    lambda x: 1 if x in bad_status else 0
)


# ----------------------------
# Remove Duplicate IDs
# ----------------------------

data = data.groupby("ID").first().reset_index()


# ----------------------------
# Fill Missing Values
# ----------------------------

data.fillna(method="ffill", inplace=True)


# ----------------------------
# Encode Categorical Columns
# ----------------------------

encoder = LabelEncoder()

for column in data.columns:

    if data[column].dtype == "object":

        data[column] = encoder.fit_transform(data[column])


# ----------------------------
# Features and Target
# ----------------------------

X = data.drop("TARGET", axis=1)

y = data["TARGET"]


# ----------------------------
# Train Test Split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42

)


# ----------------------------
# Models
# ----------------------------

models = {

    "Logistic Regression":
        LogisticRegression(max_iter=1000),

    "Decision Tree":
        DecisionTreeClassifier(),

    "Random Forest":
        RandomForestClassifier(n_estimators=100)

}


best_accuracy = 0
best_model = None


# ----------------------------
# Train Models
# ----------------------------

for name, model in models.items():

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    accuracy = accuracy_score(y_test, prediction)

    print(name, "Accuracy :", accuracy)

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_model = model


# ----------------------------
# Save Best Model
# ----------------------------

os.makedirs("model", exist_ok=True)

with open("model/best_model.pkl", "wb") as file:

    pickle.dump(best_model, file)


print("--------------------------------")

print("Best Accuracy :", best_accuracy)

print("Model Saved Successfully")

print("--------------------------------")