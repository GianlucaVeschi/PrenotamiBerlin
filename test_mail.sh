#!/bin/bash
# Test macOS mail functionality

echo "=========================================="
echo "📬 Testing macOS Mail Configuration"
echo "=========================================="
echo ""

# Check 1: Is mail command available?
echo "1️⃣  Checking if 'mail' command exists..."
if command -v mail &> /dev/null; then
    echo "   ✅ mail command found: $(which mail)"
else
    echo "   ❌ mail command not found!"
    echo "   macOS should have this by default"
fi
echo ""

# Check 2: Is Mail.app configured?
echo "2️⃣  Checking Mail.app configuration..."
MAIL_ACCOUNTS=$(defaults read com.apple.mail 2>/dev/null | grep -c "AccountPath" || echo "0")
if [ "$MAIL_ACCOUNTS" -gt 0 ]; then
    echo "   ✅ Mail.app appears to be configured (found $MAIL_ACCOUNTS account paths)"
else
    echo "   ⚠️  Mail.app may not be configured"
    echo "   The 'mail' command requires Mail.app to be set up"
fi
echo ""

# Check 3: Test sending a simple email
echo "3️⃣  Attempting to send test email via mail command..."
echo "This is a test email from Prenotami Bot troubleshooting." | mail -s "Prenotami Bot Test - $(date)" gianluca.veschi00@gmail.com
MAIL_EXIT_CODE=$?

if [ $MAIL_EXIT_CODE -eq 0 ]; then
    echo "   ✅ mail command executed successfully"
    echo "   Check your email in 1-2 minutes"
else
    echo "   ❌ mail command failed (exit code: $MAIL_EXIT_CODE)"
    echo "   Mail.app may not be configured"
fi
echo ""

# Check 4: Mail.app process
echo "4️⃣  Checking if Mail.app is running..."
if pgrep -x "Mail" > /dev/null; then
    echo "   ✅ Mail.app is running"
else
    echo "   ⚠️  Mail.app is not running"
    echo "   You may need to open Mail.app and configure it"
fi
echo ""

# Check 5: Check mail queue
echo "5️⃣  Checking mail queue..."
if command -v mailq &> /dev/null; then
    QUEUE_STATUS=$(mailq 2>&1)
    if echo "$QUEUE_STATUS" | grep -q "empty\|Mail queue is empty"; then
        echo "   ✅ Mail queue is empty (all messages sent)"
    else
        echo "   ⚠️  There are messages in the queue:"
        echo "$QUEUE_STATUS" | head -10 | sed 's/^/   /'
    fi
else
    echo "   ℹ️  mailq command not available"
fi
echo ""

echo "=========================================="
echo "📊 DIAGNOSIS"
echo "=========================================="
echo ""

if [ $MAIL_EXIT_CODE -ne 0 ]; then
    echo "❌ macOS mail command is NOT working properly"
    echo ""
    echo "This means the fallback email method isn't working."
    echo ""
    echo "🔧 RECOMMENDED SOLUTION:"
    echo "Fix the Gmail SMTP method instead (more reliable)"
    echo ""
    echo "To fix Gmail SMTP:"
    echo "  1. Enable 2FA: https://myaccount.google.com/security"
    echo "  2. Create app password: https://myaccount.google.com/apppasswords"
    echo "  3. Update .env with: GMAIL_APP_PASSWORD=your_app_password"
    echo "  4. Test: ~/VScodeProjects/PrenotamiBerlin/debug_email.sh"
else
    echo "✅ macOS mail command appears to work"
    echo ""
    echo "If you still didn't receive the email, possible reasons:"
    echo ""
    echo "1. Mail.app is not fully configured"
    echo "   → Open Mail.app and add your Gmail account"
    echo "   → Go to: Mail → Settings → Accounts"
    echo ""
    echo "2. Email is delayed (can take 5-10 minutes)"
    echo "   → Wait a bit longer and check again"
    echo ""
    echo "3. Gmail is blocking the email"
    echo "   → Check ALL folders in Gmail (not just Inbox/Spam)"
    echo ""
    echo "🔧 RECOMMENDED SOLUTION:"
    echo "Use Gmail SMTP method instead (instant delivery, more reliable)"
    echo ""
    echo "To set up Gmail SMTP:"
    echo "  1. Enable 2FA: https://myaccount.google.com/security"
    echo "  2. Create app password: https://myaccount.google.com/apppasswords"
    echo "  3. Update .env: nano ~/VScodeProjects/PrenotamiBerlin/.env"
    echo "  4. Add: GMAIL_APP_PASSWORD=your_new_app_password"
    echo "  5. Test: ~/VScodeProjects/PrenotamiBerlin/debug_email.sh"
fi

echo ""
echo "=========================================="

