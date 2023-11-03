from fastapi import FastAPI
import pandas as pd
import pickle
import numpy as np


app = FastAPI()

with open("app/column_names.pkl","rb") as columns:
    column_names = pickle.load(columns)


# Load the trained model
with open("app/model/lg_pipeline.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@app.get("/")
async def root():
    return {"Health check": "OK"}

@app.post("/predict/")
async def predict_prob_default(input_data: dict):
    # Assuming input_data is a dictionary with the required input columns
    # Example: {"feature1": 0.5, "feature2": 0.3}
    inputs = pd.DataFrame(input_data,columns=column_names,index=[0])
    prob_default = model.predict_proba(inputs)
    return {"probability_of_default": prob_default}