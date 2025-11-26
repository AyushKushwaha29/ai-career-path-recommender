from flask import Blueprint, render_template, request, jsonify
from .models import db, UserQuery
from .ml.predict import predict_roles
from .utils.skill_matching import analyze_skills
from .utils.resume_parser import extract_skills_from_pdf
from .utils.analyzer import analyze_resume_vs_jd  # Make sure this import exists
import PyPDF2

main = Blueprint('main', __name__)

# --- HOME PAGE ---
@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# --- RESUME UPLOAD API (For Auto-fill) ---
@main.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    skills = extract_skills_from_pdf(file)
    return jsonify({'extracted_skills': skills})

# --- CAREER RESULT PAGE ---
@main.route('/result', methods=['POST'])
def result():
    # 1. Gather Data from Form
    name = request.form.get('name')
    branch = request.form.get('branch')
    skills_input = request.form.get('skills') # Comma separated
    interests_input = request.form.get('interests')
    job_type = request.form.get('preferred_job_type')
    
    # 2. Prepare for ML Model
    # (The model expects space-separated strings for text fields)
    skills_list = [s.strip() for s in skills_input.split(',')]
    user_data = {
        "branch": branch,
        "skills": skills_input.replace(',', ' '), 
        "interests": interests_input.replace(',', ' '),
        "preferred_job_type": job_type
    }
    
    # 3. Get Predictions (Top 3)
    predictions = predict_roles(user_data)
    
    results_data = []
    
    # 4. Detailed Analysis for each role
    for role, prob in predictions:
        analysis = analyze_skills(skills_list, role)
        analysis['probability'] = round(prob * 100, 1)
        results_data.append(analysis)
        
    # 5. Save to DB (Optional - wrapped in try/except to prevent crashes)
    try:
        if name:
            new_query = UserQuery(name=name, skills=skills_input, predicted_role=predictions[0][0])
            db.session.add(new_query)
            db.session.commit()
    except Exception as e:
        print(f"Database error: {e}")
    
    # CRITICAL FIX: This return statement must be here!
    return render_template('result.html', user_name=name, results=results_data)


# --- RESUME ANALYZER PAGES ---

@main.route('/analyzer', methods=['GET'])
def analyzer_page():
    return render_template('analyze.html')

@main.route('/analyze-result', methods=['POST'])
def analyze_result():
    if 'resume' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['resume']
    jd_text = request.form.get('jd_text')
    
    if file.filename == '':
        return "No file selected", 400

    # Extract raw text for analysis
    # (We can't use the simple skill extractor here, we need full text)
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text() + " "
    except Exception as e:
        return f"Error reading PDF: {e}", 400
        
    # Run Analysis
    analysis = analyze_resume_vs_jd(resume_text, jd_text)
    
    return render_template('analysis_result.html', result=analysis)