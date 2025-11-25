# AI Career Path Recommender & Skill Gap Analyzer

A full-stack web application that helps students and professionals identify suitable tech career paths using Machine Learning. It analyzes user skills (via manual input or Resume PDF), recommends top roles, visualizes skill gaps, and provides tailored learning roadmaps.

## Features
- **AI-Based Recommendations**: Uses a Random Forest Classifier trained on synthetic career data.
- **Resume Parsing**: Extracts skills from PDF resumes automatically using PyPDF2.
- **Skill Gap Analysis**: visualizes missing skills vs. required skills for target roles.
- **Interactive Roadmaps**: Step-by-step weekly learning guides for recommended roles.
- **Dashboard**: Clean UI with Chart.js visualizations.

## Tech Stack
- **Backend**: Python, Flask, SQLAlchemy
- **ML**: Scikit-learn, Pandas, NumPy
- **Frontend**: HTML5, Bootstrap 5, Chart.js
- **Utils**: PyPDF2 (PDF parsing)

## Setup Instructions

1. **Clone the repository** (or create folders as per structure).

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate