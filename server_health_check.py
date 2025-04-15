import psutil
import smtplib
import time
import datetime
import logging
import os
from email.mime.text import MIMEText

# Set up logging to track system activity (like a backup system)
logging.basicConfig(filename='server_health.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Simulated Active Directory user database (simple dictionary for demo)
users = {
    "admin": {"role": "admin", "last_login": "2025-04-15 08:00:00"},
    "user1": {"role": "user", "last_login": "2025-04-15 09:00:00"}
}

def check_system_health():
    """Check CPU, memory, and disk usage like a daily health check."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    health_report = (
        f"CPU Usage: {cpu_usage}%\n"
        f"Memory Usage: {memory.percent}% ({memory.used/1024**3:.2f} GB used)\n"
        f"Disk Usage: {disk.percent}% ({disk.used/1024**3:.2f} GB used)"
    )
    logging.info("System health check completed:\n" + health_report)
    return health_report

def simulate_ad_management():
    """Simulate Active Directory tasks like checking user status."""
    suspicious_activity = False
    for user, info in users.items():
        last_login = datetime.datetime.strptime(info["last_login"], "%Y-%m-%d %H:%M:%S")
        if (datetime.datetime.now() - last_login).total_seconds() < 300:  # Recent login < 5 min
            suspicious_activity = True
            logging.warning(f"Suspicious login detected for {user}")
    ad_report = "AD Check: " + ("Suspicious activity detected!" if suspicious_activity else "All users normal.")
    logging.info(ad_report)
    return ad_report

def generate_report():
    """Generate a combined report for health and AD checks."""
    health_report = check_system_health()
    ad_report = simulate_ad_management()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = (
        f"Server Health Report - {timestamp}\n\n"
        f"===== System Health =====\n{health_report}\n\n"
        f"===== Active Directory =====\n{ad_report}"
    )
    return report

def send_report_email(report):
    """Send the report via email (simulates FTP and batch scheduling)."""
    sender = "charlesmaponya64@gmail.com"  # Replace with your Gmail
    receiver = "charlesmaponya64@gmail.com"  # Replace with your email or a test email
    password = "rild fgzp qejx pdtc"  # Replace with your app-specific password
    
    msg = MIMEText(report)
    msg['Subject'] = 'Daily Server Health Report'
    msg['From'] = sender
    msg['To'] = receiver
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        logging.info("Report email sent successfully")
        return "Report sent successfully!"
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        return f"Failed to send email: {str(e)}"

def main():
    try:
        print("Starting the script...")
        logging.info("Starting server health check system")
        print("Generating report...")
        report = generate_report()
        print("Report generated successfully!")
        print(report)
        email_status = send_report_email(report)
        print(email_status)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()