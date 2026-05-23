FROM python:3.10-slim
WORKDIR /app
RUN pip install pandas scikit-learn mlflow joblib
COPY src/ /app/src/
COPY model/ /app/model/
EXPOSE 80
CMD ["python", "-m", "http.server", "80"]
