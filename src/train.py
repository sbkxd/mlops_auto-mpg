import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
import joblib
import os

os.makedirs("model", exist_ok=True)
column_names = ["mpg", "cylinders", "displacement", "horsepower", "weight", "acceleration", "model_year", "origin", "car_name"]
df = pd.read_csv("Dataset/auto-mpg.data", delim_whitespace=True, names=column_names)

df = df[df.horsepower != '?']
df.horsepower = df.horsepower.astype(float)
X = df.drop(["mpg", "car_name"], axis=1)
y = df["mpg"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

with mlflow.start_run():
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    mlflow.log_param("test_size", 0.2)
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("r2", r2)
    mlflow.sklearn.log_model(model, "model")
    
    joblib.dump(model, "model/model.pkl")
    print(f"Model trained successfully. MSE: {mse:.4f}, R2: {r2:.4f}")
