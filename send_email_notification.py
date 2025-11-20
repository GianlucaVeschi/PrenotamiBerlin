#!/usr/bin/env python3
"""
Email notification script for Prenotami Bot
Sends email with bot execution results
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# Configuration
RECIPIENT_EMAIL = "gianluca.veschi00@gmail.com"
SENDER_EMAIL = "gianluca.veschi00@gmail.com"  # Same as recipient for Gmail
PROJECT_DIR = Path("/Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin")

def read_last_lines(file_path, num_lines=20):
    """Read last N lines from a file"""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            return ''.join(lines[-num_lines:])
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error reading file: {e}"

def check_for_slots():
    """Check if any slots were found"""
    log_file = PROJECT_DIR / "prenotami_bot.log"
    try:
        with open(log_file, 'r') as f:
            content = f.read()
            if "Found" in content and "available slot" in content:
                return True, "🎉 AVAILABLE SLOT FOUND!"
            elif "No available slots" in content or "esauriti" in content:
                return False, "No slots available (will try again tomorrow)"
            else:
                return None, "Status unclear - check logs"
    except:
        return None, "Could not check slot status"

def count_todays_screenshots():
    """Count screenshots from today"""
    today = datetime.now().strftime("%Y%m%d")
    screenshots = list(PROJECT_DIR.glob(f"screenshot_*{today}*.png"))
    return len(screenshots)

def get_current_day():
    """Get current day of 3-day cycle"""
    start_file = PROJECT_DIR / ".cron_start_date"
    if not start_file.exists():
        return "Not started yet"
    
    try:
        import time
        start_date = int(start_file.read_text().strip())
        current_date = int(time.time())
        days_elapsed = (current_date - start_date) // 86400
        return f"Day {days_elapsed + 1} of 3"
    except:
        return "Unknown"

def create_email_body():
    """Create the email body with bot results"""
    slot_found, slot_status = check_for_slots()
    screenshot_count = count_todays_screenshots()
    current_day = get_current_day()
    
    # Read logs
    cron_log = read_last_lines(PROJECT_DIR / "cron_bot.log", 10)
    bot_log = read_last_lines(PROJECT_DIR / "prenotami_bot.log", 20)
    
    # Create email body
    body = f"""
Prenotami Bot - Execution Report
{'='*60}

📅 Date: {datetime.now().strftime("%A, %B %d, %Y at %H:%M")}
📊 Status: {current_day}

{'='*60}
RESULTS
{'='*60}

🎯 Slot Availability: {slot_status}
📸 Screenshots Created: {screenshot_count}

{'='*60}
CRON EXECUTION LOG (Last 10 lines)
{'='*60}

{cron_log}

{'='*60}
BOT EXECUTION LOG (Last 20 lines)
{'='*60}

{bot_log}

{'='*60}
"""
    
    if slot_found:
        body += """
🚨 ACTION REQUIRED! 🚨

AN APPOINTMENT SLOT WAS FOUND!

Next Steps:
1. Log into: https://prenotami.esteri.it/
2. Navigate to Prenota → ID Card booking
3. Complete the booking IMMEDIATELY!
4. Check screenshots in the project folder for details

Time is critical - act now!

"""
    else:
        body += """
ℹ️  No slots available yet.

The bot will automatically run again tomorrow at 7:00 AM.
No action needed from you.

"""
    
    body += f"""
{'='*60}
SCREENSHOTS LOCATION
{'='*60}

{PROJECT_DIR}/screenshot_*.png

{'='*60}

This is an automated message from your Prenotami Bot.
"""
    
    return body, slot_found

def send_email_gmail(subject, body):
    """
    Send email using Gmail SMTP
    Requires app password (not regular Gmail password)
    """
    # Check for app password in environment or .env file
    app_password = os.getenv('GMAIL_APP_PASSWORD')
    
    if not app_password:
        print("⚠️  Gmail app password not configured")
        print("Please see EMAIL_SETUP.md for instructions")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, app_password)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent successfully to {RECIPIENT_EMAIL}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def send_email_macos_mail(subject, body):
    """
    Fallback: Use macOS mail command
    Requires Mail.app to be configured
    """
    try:
        import subprocess
        
        # Create temporary file with email body
        temp_file = PROJECT_DIR / ".email_temp.txt"
        with open(temp_file, 'w') as f:
            f.write(body)
        
        # Send using mail command
        cmd = f'cat {temp_file} | mail -s "{subject}" {RECIPIENT_EMAIL}'
        result = subprocess.run(cmd, shell=True, capture_output=True)
        
        # Clean up
        temp_file.unlink()
        
        if result.returncode == 0:
            print(f"✅ Email sent successfully to {RECIPIENT_EMAIL}")
            return True
        else:
            print(f"⚠️  Mail command failed: {result.stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to send email via mail command: {e}")
        return False

def main():
    """Main function"""
    print("📧 Preparing email notification...")
    
    # Create email body
    body, slot_found = create_email_body()
    
    # Create subject based on results
    if slot_found:
        subject = "🎉 PRENOTAMI BOT: SLOT FOUND! - Action Required"
    else:
        current_day = get_current_day()
        subject = f"Prenotami Bot Report - {current_day} - No slots yet"
    
    print(f"Subject: {subject}")
    print(f"Recipient: {RECIPIENT_EMAIL}")
    
    # Try to send email
    # First try Gmail SMTP (more reliable)
    success = send_email_gmail(subject, body)
    
    # If Gmail fails, try macOS mail command
    if not success:
        print("Trying fallback method (macOS mail)...")
        success = send_email_macos_mail(subject, body)
    
    if success:
        print("✅ Email notification sent!")
        # Log the email send
        log_file = PROJECT_DIR / "cron_bot.log"
        with open(log_file, 'a') as f:
            f.write(f"{datetime.now()}: Email notification sent to {RECIPIENT_EMAIL}\n")
    else:
        print("❌ Failed to send email notification")
        print("Check EMAIL_SETUP.md for configuration instructions")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

