import os
import smtplib
import logging
from email.message import EmailMessage
from typing import Dict, Any

def generate_html_report(data: Dict[str, Any]) -> str:
    """Generates an HTML report from the DeepSeek analyzed data."""
    if not data or not data.get("top_10_attacks"):
        return "<p>No significant cyber attacks were found in today's news.</p>"

    html = "<html><body>"
    html += "<h2>Daily Top 10 Cyber Attacks Report</h2>"
    
    # Top 10 Table
    html += "<table border='1' cellpadding='5' cellspacing='0'>"
    html += "<tr style='background-color:#f2f2f2'><th>Rank</th><th>Title</th><th>Source</th><th>Summary</th></tr>"
    
    for attack in data.get("top_10_attacks", []):
        html += f"<tr>"
        html += f"<td>{attack.get('rank', '-')}</td>"
        html += f"<td><a href='{attack.get('link', '#')}'>{attack.get('title', 'N/A')}</a></td>"
        html += f"<td>{attack.get('source', 'N/A')}</td>"
        html += f"<td>{attack.get('summary', 'N/A')}</td>"
        html += f"</tr>"
    
    html += "</table><br><br>"
    
    # Teaching Lessons
    html += "<h2>Teaching Lessons for Top 2 Attacks</h2>"
    for lesson in data.get("lessons", []):
        html += f"<div style='border:1px solid #ccc; padding:10px; margin-bottom:15px;'>"
        html += f"<h3>Rank #{lesson.get('rank', '-')} - {lesson.get('title', 'N/A')}</h3>"
        
        html += "<h4>Learning Objectives:</h4><ul>"
        for obj in lesson.get("learning_objectives", []):
            html += f"<li>{obj}</li>"
        html += "</ul>"
        
        html += f"<h4>Real-World Impact:</h4><p>{lesson.get('real_world_impact', 'N/A')}</p>"
        
        html += "<h4>Mitigation Strategies:</h4><ul>"
        for strategy in lesson.get("mitigation_strategies", []):
            html += f"<li>{strategy}</li>"
        html += "</ul>"
        
        html += "<h4>Discussion Questions:</h4><ul>"
        for qs in lesson.get("discussion_questions", []):
            html += f"<li>{qs}</li>"
        html += "</ul>"
        html += "</div>"
        
    html += "</body></html>"
    return html

def send_email_report(data: Dict[str, Any]):
    """Sends the formatted HTML report via SMTP."""
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    
    if not all([smtp_server, smtp_user, smtp_pass, receiver_email]):
        logging.error("Missing required SMTP environment variables. Email will not be sent.")
        return
        
    html_content = generate_html_report(data)
    
    msg = EmailMessage()
    msg['Subject'] = "Daily Cyber Attack Report & Teaching Lessons"
    msg['From'] = smtp_user
    msg['To'] = receiver_email
    
    msg.add_alternative(html_content, subtype='html')
    
    try:
        logging.info(f"Connecting to SMTP server {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        logging.info(f"Report successfully sent to {receiver_email}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def send_telegram_message(data: Dict[str, Any]):
    """Sends a summary report via Telegram Bot."""
    import requests
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id or bot_token == "your_telegram_bot_token_here":
        logging.error("Missing valid TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID. Telegram message will not be sent.")
        return

    # Create a concise summary for Telegram
    message = "🚨 *Daily Cyber Attack Report* 🚨\n\n"
    
    top_attacks = data.get("top_10_attacks", [])
    if not top_attacks:
        message += "No significant cyber attacks were found in today's news."
    else:
        message += f"Found {len(top_attacks)} critical threats today.\n\n*Top 3 Threats:*\n"
        for i, attack in enumerate(top_attacks[:3]):
            message += f"{i+1}. [{attack.get('title')}]({attack.get('link')})\n"
            
        message += "\n*Lessons Generated:* "
        message += "Yes ✅\n" if data.get("lessons") else "No ❌\n"
        
        message += "\nDashboard updated. Please check the Web UI or your email for the full report and teaching lessons!"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logging.info("Telegram notification sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {e}")

if __name__ == "__main__":
    # Test HTML Generation
    mock_data = {
        "top_10_attacks": [
            {"rank": 1, "title": "Test Exploit", "source": "Test Source", "link": "http://example.com", "summary": "Bad vulnerability."}
        ],
        "lessons": [
            {
                "rank": 1, "title": "Test Exploit", 
                "learning_objectives": ["Understand X"], 
                "real_world_impact": "Could cause downtime.", 
                "mitigation_strategies": ["Patch X"], 
                "discussion_questions": ["Why is X bad?"]
            }
        ]
    }
    print("Notifier module ready. Sample HTML length:", len(generate_html_report(mock_data)))
