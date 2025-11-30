import random

# SYSTEM PROMPT (If you connect to real AI)
SYSTEM_PROMPT = """
You are an expert technical interviewer. 
Your goal is to interview the user for the role of {role} ({level} level).
1. Ask one concise technical or behavioral question at a time.
2. Wait for the user's answer.
3. Provide short feedback (Good/Bad) and then ask the next question.
4. If the user says "End Interview", provide a final score (0-100) and 3 tips.
"""

# --- MOCK AI FUNCTION (Use this for testing without paying for API) ---
def get_ai_response(user_message, session_history, role, level):
    """
    This is a simulation. Replace this logic with OpenAI/Gemini API call 
    for real intelligence.
    """
    msg = user_message.lower()
    
    # Simple keyword-based simulation
    if "start" in msg:
        return f"Hello! I am your AI interviewer. Let's start your {level} {role} interview. First question: Tell me about yourself and your experience with {role}."
    
    if "end" in msg or "stop" in msg:
        return "INTERVIEW_END: Thank you. Based on our chat, I'd give you a Score: 75/100. Tip: Be more specific about your project experience."

    # Random generic questions based on role (Simulation)
    questions = [
        f"Can you explain a challenging bug you fixed in {role}?",
        "What is the difference between SQL and NoSQL?",
        "How do you handle tight deadlines?",
        "Explain the concept of Big O notation.",
        "How would you design a scalable system?"
    ]
    
    feedback = random.choice(["Good point.", "That's a valid answer.", "Could be more detailed, but okay."])
    next_q = random.choice(questions)
    
    return f"{feedback} Next Question: {next_q}"

# --- REAL AI INTEGRATION (Uncomment to use OpenAI) ---
# import openai
# openai.api_key = "YOUR_API_KEY"
# def get_real_ai_response(user_message, history, role, level):
#     messages = [{"role": "system", "content": SYSTEM_PROMPT.format(role=role, level=level)}]
#     # Add history...
#     response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
#     return response.choices[0].message.content