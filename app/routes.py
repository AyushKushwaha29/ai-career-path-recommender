from flask import Blueprint, render_template, request, jsonify
from .ml.predict import predict_roles
from .utils.skill_matching import analyze_skills
from .utils.resume_parser import extract_skills_from_pdf
from .models import db, UserQuery

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    skills = extract_skills_from_pdf(file)
    return jsonify({'extracted_skills': skills})

@main.route('/result', methods=['POST'])
def result():
    # 1. Gather Data
    name = request.form.get('name')
    branch = request.form.get('branch')
    skills_input = request.form.get('skills') # Comma separated
    interests_input = request.form.get('interests')
    job_type = request.form.get('preferred_job_type')
    
    # Prepare for ML
    # (The model expects space-separated strings for text fields)
    skills_list = [s.strip() for s in skills_input.split(',')]
    user_data = {
        "branch": branch,
        "skills": skills_input.replace(',', ' '), 
        "interests": interests_input.replace(',', ' '),
        "preferred_job_type": job_type
    }
    
    # 2. Get Predictions (Top 3)
    # returns [('Role', 0.85), ('Role2', 0.10), ...]
    predictions = predict_roles(user_data)
    
    results_data = []
    
    # 3. Detailed Analysis for each role
    for role, prob in predictions:
        analysis = analyze_skills(skills_list, role)
        analysis['probability'] = round(prob * 100, 1)
        results_data.append(analysis)
        
    # Save to DB (Optional)
    new_query = UserQuery(name=name, skills=skills_input, predicted_role=predictions[0][0])
    db.session.add(new_query)
    db.session.commit()
    
    return render_template('result.html', user_name=name, results=results_data)