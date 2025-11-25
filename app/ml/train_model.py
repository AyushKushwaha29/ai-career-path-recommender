import pandas as pd
import numpy as np
import joblib
import os
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# 1. Generate Synthetic Dataset
def generate_data(num_rows=600):
    branches = ['CSE', 'IT', 'ECE', 'ME', 'Civil']
    job_types = ['Remote', 'Office', 'Hybrid']
    
    # Role mappings to generate somewhat realistic data
    roles_skills = {
        "Backend Developer": ["Python", "Java", "SQL", "Django", "Flask", "API", "Database"],
        "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Angular", "UI/UX"],
        "Data Scientist": ["Python", "Statistics", "Pandas", "Machine Learning", "Data Analysis", "SQL"],
        "DevOps Engineer": ["Linux", "Docker", "Kubernetes", "AWS", "CI/CD", "Cloud"],
        "Machine Learning Engineer": ["Python", "Deep Learning", "TensorFlow", "PyTorch", "NLP", "CV"]
    }

    data = []
    for _ in range(num_rows):
        role = random.choice(list(roles_skills.keys()))
        branch = "CSE" if random.random() > 0.3 else random.choice(branches) # Bias towards CSE
        
        # Pick 3-5 random skills from the role + 1 random noise skill
        core_skills = random.sample(roles_skills[role], k=random.randint(3, 5))
        noise_skills = ["Excel", "Communication", "Management"]
        all_skills = core_skills + [random.choice(noise_skills)]
        random.shuffle(all_skills)
        
        interests = [role.split()[0], "Tech", "Innovation"]
        
        data.append({
            "branch": branch,
            "skills": " ".join(all_skills), # Space separated for Vectorizer
            "interests": " ".join(interests),
            "preferred_job_type": random.choice(job_types),
            "job_role": role
        })
    
    return pd.DataFrame(data)

# 2. Train Model
def train_and_save():
    print("Generating synthetic data...")
    df = generate_data()
    
    X = df[['branch', 'skills', 'interests', 'preferred_job_type']]
    y = df['job_role']

    # Preprocessing Pipeline
    # Branch & Job Type -> OneHot
    # Skills & Interests -> CountVectorizer (Bag of Words)
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['branch', 'preferred_job_type']),
            ('txt_skills', CountVectorizer(), 'skills'),
            ('txt_interests', CountVectorizer(), 'interests')
        ]
    )

    model = make_pipeline(preprocessor, RandomForestClassifier(n_estimators=100, random_state=42))

    print("Training model...")
    model.fit(X, y)

    # Save
    save_path = os.path.join(os.path.dirname(__file__), 'career_model.pkl')
    joblib.dump(model, save_path)
    print(f"Model saved to {save_path}")

if __name__ == "__main__":
    train_and_save()