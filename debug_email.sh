#!/bin/bash
# Email debugging script - diagnose email notification issues

echo "=========================================="
echo "📧 Email Notification Debugger"
echo "=========================================="
echo ""

PROJECT_DIR="/Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin"
cd "$PROJECT_DIR"

# Check 1: .env file exists
echo "1️⃣  Checking .env file..."
if [ -f "${PROJECT_DIR}/.env" ]; then
    echo "   ✅ .env file exists"
else
    echo "   ❌ .env file not found!"
    echo "   Please create it first"
    exit 1
fi
echo ""

# Check 2: GMAIL_APP_PASSWORD is set
echo "2️⃣  Checking GMAIL_APP_PASSWORD in .env..."
if grep -q "^GMAIL_APP_PASSWORD=" "${PROJECT_DIR}/.env"; then
    PASSWORD_LINE=$(grep "^GMAIL_APP_PASSWORD=" "${PROJECT_DIR}/.env")
    PASSWORD_VALUE=$(echo "$PASSWORD_LINE" | cut -d'=' -f2)
    PASSWORD_LENGTH=${#PASSWORD_VALUE}
    
    if [ "$PASSWORD_LENGTH" -gt 0 ]; then
        echo "   ✅ GMAIL_APP_PASSWORD is set (${PASSWORD_LENGTH} characters)"
        
        # Show masked password
        MASKED_PASSWORD=$(echo "$PASSWORD_VALUE" | sed 's/./*/g')
        echo "   Value: $MASKED_PASSWORD"
        
        # Check if it looks like it might have spaces
        if [[ "$PASSWORD_VALUE" == *" "* ]]; then
            echo "   ⚠️  WARNING: Password contains spaces! Remove them."
        fi
    else
        echo "   ❌ GMAIL_APP_PASSWORD is empty!"
        echo "   Please add your Gmail app password to .env"
    fi
else
    echo "   ❌ GMAIL_APP_PASSWORD not found in .env!"
    echo "   Please add: GMAIL_APP_PASSWORD=your_password"
fi
echo ""

# Check 3: Python dependencies
echo "3️⃣  Checking Python environment..."
if [ -d "${PROJECT_DIR}/venv" ]; then
    echo "   ✅ Virtual environment exists"
    source "${PROJECT_DIR}/venv/bin/activate"
    echo "   ✅ Virtual environment activated"
else
    echo "   ❌ Virtual environment not found!"
    exit 1
fi
echo ""

# Check 4: Test loading environment variables
echo "4️⃣  Testing environment variable loading..."
python3 << 'EOF'
import os
from dotenv import load_dotenv
from pathlib import Path

project_dir = Path("/Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin")
env_file = project_dir / ".env"

print(f"   Loading from: {env_file}")
load_dotenv(env_file)

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
gmail_password = os.getenv('GMAIL_APP_PASSWORD')

if email:
    print(f"   ✅ EMAIL loaded: {email}")
else:
    print("   ❌ EMAIL not loaded")

if password:
    print(f"   ✅ PASSWORD loaded: {'*' * len(password)}")
else:
    print("   ❌ PASSWORD not loaded")

if gmail_password:
    print(f"   ✅ GMAIL_APP_PASSWORD loaded: {'*' * len(gmail_password)} ({len(gmail_password)} chars)")
else:
    print("   ❌ GMAIL_APP_PASSWORD not loaded")
EOF
echo ""

# Check 5: Test SMTP connection
echo "5️⃣  Testing Gmail SMTP connection..."
python3 << 'EOF'
import smtplib
import os
from dotenv import load_dotenv
from pathlib import Path

project_dir = Path("/Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin")
load_dotenv(project_dir / ".env")

email = os.getenv('EMAIL')
gmail_password = os.getenv('GMAIL_APP_PASSWORD')

if not gmail_password:
    print("   ❌ GMAIL_APP_PASSWORD not set")
    exit(1)

if not email:
    print("   ❌ EMAIL not set")
    exit(1)

try:
    print(f"   Connecting to smtp.gmail.com:587...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    print("   ✅ Connected to SMTP server")
    
    print("   Starting TLS...")
    server.starttls()
    print("   ✅ TLS started")
    
    print(f"   Logging in as {email}...")
    server.login(email, gmail_password)
    print("   ✅ Login successful!")
    
    server.quit()
    print("   ✅ SMTP connection test passed!")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"   ❌ Authentication failed!")
    print(f"   Error: {e}")
    print("")
    print("   Possible causes:")
    print("   - Wrong app password")
    print("   - Using regular Gmail password instead of app password")
    print("   - 2FA not enabled on Google account")
    print("   - App password was revoked")
    
except smtplib.SMTPException as e:
    print(f"   ❌ SMTP error: {e}")
    
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    print("")
    print("   Possible causes:")
    print("   - No internet connection")
    print("   - Firewall blocking port 587")
    print("   - Gmail SMTP is down")
EOF
echo ""

# Check 6: Try sending actual test email
echo "6️⃣  Attempting to send test email..."
python3 "${PROJECT_DIR}/send_email_notification.py"
echo ""

# Check 7: Check logs for errors
echo "7️⃣  Checking recent logs..."
if [ -f "${PROJECT_DIR}/cron_bot.log" ]; then
    echo "   Recent cron_bot.log entries:"
    tail -5 "${PROJECT_DIR}/cron_bot.log" | sed 's/^/   /'
else
    echo "   No cron_bot.log found yet"
fi
echo ""

# Summary
echo "=========================================="
echo "📊 DIAGNOSIS SUMMARY"
echo "=========================================="
echo ""
echo "If email test failed, common issues:"
echo ""
echo "1. Wrong app password"
echo "   → Go to https://myaccount.google.com/apppasswords"
echo "   → Generate new app password"
echo "   → Update .env file"
echo ""
echo "2. Using regular Gmail password"
echo "   → You MUST use an app password, not your Gmail password"
echo ""
echo "3. 2FA not enabled"
echo "   → Enable 2-Factor Authentication on Google account"
echo "   → Then create app password"
echo ""
echo "4. Password has spaces"
echo "   → Remove all spaces from the password in .env"
echo ""
echo "5. Internet/firewall issues"
echo "   → Check internet connection"
echo "   → Check if port 587 is blocked"
echo ""
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Review the output above"
echo "  2. Fix any ❌ issues found"
echo "  3. Run this script again to verify"
echo "  4. Check spam folder if email sent successfully"
echo ""

