from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

SENDER_EMAIL = os.getenv("GMAIL_USER")
SENDER_PASSWORD = os.getenv("GMAIL_PASS")

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/send-email")
async def send_email(
    request: Request,
    email_id: str = Form(...),
    receiver_name: str = Form(...),
    position: str = Form(...),
    linkedin: str = Form(...),
    github: str = Form(...)
):
    subject = f"Applying for {position}"
    greeting = f"Hi {receiver_name}," if receiver_name.strip() else "Dear Hiring Manager,"

    body = f"""
{greeting}

I am writing to express my interest in the {position} role. With 3.7+ years of professional experience building scalable, secure, and production-ready web applications using Python and Django REST Framework, I bring strong expertise in backend engineering and cloud deployment.

At DreamzTech Solutions, I led backend development for education and analytics platforms used by over 1,000 active users monthly. My work involved implementing role-based access with JWT, integrating third-party APIs like Wonde, and deploying on AWS EC2. I’ve also worked on report automation with Celery + Redis, and delivered PDF/Excel reporting modules for various domains.

Prior to that, I contributed to IT automation systems at Stackup Technologies and built reusable job orchestration APIs using Django and PostgreSQL. My approach is focused on performance, clean code, and security.

My current CTC is 8.28 LPA, and I am an immediate joiner. I’m actively seeking my next challenge to build high-impact platforms and collaborate with strong tech teams.

Please find my resume attached. I would welcome the opportunity to discuss how my experience aligns with your team’s goals.

Best regards,  
Bimalendu Swain  
📞 +91 98614 84514  
📧 bimalenduswain07@gmail.com  
🔗 LinkedIn: {linkedin}  
🔗 GitHub: {github}
"""

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = email_id
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with open("CV_Bimalendu_Swain.pdf", "rb") as file:
            part = MIMEApplication(file.read(), Name="CV_Bimalendu_Swain.pdf")
            part['Content-Disposition'] = 'attachment; filename="CV_Bimalendu_Swain.pdf"'
            message.attach(part)
    except FileNotFoundError:
        return templates.TemplateResponse("form.html", {"request": request, "status": "Resume file not found!"})

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(message)
        status = "✅ Email sent successfully!"
    except Exception as e:
        status = f"Error sending email: {str(e)}"

    return templates.TemplateResponse("form.html", {"request": request, "status": status})
