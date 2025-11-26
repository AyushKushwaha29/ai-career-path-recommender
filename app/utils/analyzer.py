import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text):
    # Text ko lowercase aur special characters remove karne ke liye
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def analyze_resume_vs_jd(resume_text, jd_text):
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(jd_text)
    
    # 1. ATS Match Score Calculate karna (Cosine Similarity)
    text_list = [cleaned_resume, cleaned_jd]
    cv = CountVectorizer(stop_words='english')
    count_matrix = cv.fit_transform(text_list)
    
    # Similarity score (0 se 1 ke beech hota hai, hum % mein convert karenge)
    match_percentage = cosine_similarity(count_matrix)[0][1] * 100
    match_percentage = round(match_percentage, 2)
    
    # 2. Missing Keywords dhoondna
    # Hum un words ko nikalenge jo JD mein hain par Resume mein nahi
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform([cleaned_jd])
    jd_keywords = vectorizer.get_feature_names_out()
    
    missing_keywords = []
    for word in jd_keywords:
        if word not in cleaned_resume:
            missing_keywords.append(word)
            
    # Sirf top 10 missing keywords return karte hain taaki user overwhelm na ho
    # (Optional: Aap isse refine kar sakte hain frequency ke hisaab se)
    
    return {
        "match_percentage": match_percentage,
        "missing_keywords": missing_keywords[:10], # Top 10 missing
        "word_count": len(cleaned_resume.split())
    }