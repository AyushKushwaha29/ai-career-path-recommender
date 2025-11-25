import PyPDF2 # type: ignore
import re
import io

# A basic list of tech skills to look for (expand this in production)
KNOWN_SKILLS = [
    "python", "java", "c++", "javascript", "typescript", "html", "css", "sql", 
    "react", "angular", "vue", "node", "django", "flask", "fastapi", 
    "docker", "kubernetes", "aws", "azure", "linux", "git", 
    "machine learning", "deep learning", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "nlp", "opencv"
]

def extract_skills_from_pdf(pdf_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text().lower() + " "
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []

    # Extract skills
    found_skills = set()
    # Simple keyword matching
    for skill in KNOWN_SKILLS:
        # Regex to find skill as a whole word
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.add(skill)
            
    return list(found_skills)