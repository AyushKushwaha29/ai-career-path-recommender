import joblib
import pandas as pd
import os

model_path = os.path.join(os.path.dirname(__file__), 'career_model.pkl')
model = None

def load_model():
    global model
    if model is None:
        if os.path.exists(model_path):
            model = joblib.load(model_path)
        else:
            raise Exception("Model not found. Run app/ml/train_model.py first.")

def predict_roles(user_data):
    """
    user_data: dict with keys ['branch', 'skills', 'interests', 'preferred_job_type']
    Returns: List of tuples [('Role', probability), ...]
    """
    load_model()
    
    # Convert user input dict to DataFrame
    df = pd.DataFrame([user_data])
    
    # Get probabilities
    probs = model.predict_proba(df)[0]
    classes = model.classes_
    
    # Create list of (Role, Prob)
    role_probs = list(zip(classes, probs))
    
    # Sort by probability descending
    role_probs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 3
    return role_probs[:3]