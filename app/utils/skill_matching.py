import json
import os

# Load configs
BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, 'job_roles_config.json')) as f:
    JOB_ROLES = json.load(f)

with open(os.path.join(BASE_DIR, 'roadmaps_config.json')) as f:
    ROADMAPS = json.load(f)

def analyze_skills(user_skills_list, role_name):
    """
    Compares user skills with role requirements.
    """
    role_data = JOB_ROLES.get(role_name, {})
    required = set(s.lower() for s in role_data.get("required_skills", []))
    
    # Normalize user skills
    user_set = set(s.lower().strip() for s in user_skills_list)
    
    matched = list(required.intersection(user_set))
    missing = list(required.difference(user_set))
    
    # Calculate simple match percentage
    if not required:
        score = 0
    else:
        score = int((len(matched) / len(required)) * 100)
        
    return {
        "role": role_name,
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "roadmap": ROADMAPS.get(role_name, None)
    }