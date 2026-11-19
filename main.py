import os
import re
import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURATION (Loaded from GitHub Secrets) ---
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")       # Your Gmail address (e.g., sharmaguddu7794@gmail.com)
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD") # Your 16-character Gmail App Password

def search_linkedin_posts():
    url = "https://google.serper.dev/search"
    
    # Keywords and US-based filter from the task requirements
    query = 'site:linkedin.com/posts ("Java Developer") ("C2C" OR "Bench" OR "Sales" OR "W2" OR "Full-Time" OR "Hotlist") ("USA" OR "US" OR "United States")'
    
    payload = json.dumps({
        "q": query,
        "gl": "us",       # Restricts search to US-based results
        "tbs": "qdr:d",   # Filters posts from the last 24 hours
        "num": 30         # Fetches top 30 matching posts
    })
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json().get("organic", [])
    else:
        print("API Error:", response.text)
        return []

def extract_emails(text):
    # Regex pattern to extract email addresses from post text
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return list(set(re.findall(email_pattern, text)))

def send_email(to_email, post_link):
    subject = "Application for Java Developer Role (C2C / W2 / Full-Time)"
    
    # Update this body with the exact email template provided by your team
    body = f"""Hi Hiring Team,

I came across your recent LinkedIn post regarding the Java Developer requirement ({post_link}). 

We have experienced Java Developers available immediately for C2C / W2 / Full-Time roles across the US. Please share the job description or let me know a good time to connect.

Best Regards,
Guddu Kumar
"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[SUCCESS