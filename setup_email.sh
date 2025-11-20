#!/bin/bash
# Helper script to configure email notifications

echo "=========================================="
echo "📧 Email Notification Setup"
echo "=========================================="
echo ""

PROJECT_DIR="/Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin"
ENV_FILE="${PROJECT_DIR}/.env"

# Check if .env exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ .env file not found!"
    echo "Please create it first with your Prenotami credentials"
    exit 1
fi

echo "To enable email notifications, you need a Gmail App Password."
echo ""
echo "📋 Steps to get your App Password:"
echo "  1. Go to: https://myaccount.google.com/apppasswords"
echo "  2. Sign in to gianluca.veschi00@gmail.com"
echo "  3. Create a new app password for 'Mail'"
echo "  4. Copy the 16-character password (remove spaces)"
echo ""
echo "📖 Full instructions: See EMAIL_SETUP.md"
echo ""

# Check if already configured
if grep -q "GMAIL_APP_PASSWORD" "$ENV_FILE"; then
    echo "ℹ️  GMAIL_APP_PASSWORD already exists in .env"
    echo ""
    read -p "Do you want to update it? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing password."
        exit 0
    fi
fi

echo ""
read -p "Enter your Gmail App Password (16 characters, no spaces): " app_password

# Validate format (should be at least 8 characters)
if [ ${#app_password} -lt 8 ]; then
    echo ""
    echo "⚠️  Warning: App password should be at least 8 characters"
    echo "You entered: ${#app_password} characters"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
fi

# Add or update the password in .env
if grep -q "GMAIL_APP_PASSWORD" "$ENV_FILE"; then
    # Update existing line
    sed -i '' "s/^GMAIL_APP_PASSWORD=.*/GMAIL_APP_PASSWORD=$app_password/" "$ENV_FILE"
    echo "✅ Updated GMAIL_APP_PASSWORD in .env"
else
    # Add new line
    echo "" >> "$ENV_FILE"
    echo "# Gmail App Password for email notifications" >> "$ENV_FILE"
    echo "GMAIL_APP_PASSWORD=$app_password" >> "$ENV_FILE"
    echo "✅ Added GMAIL_APP_PASSWORD to .env"
fi

echo ""
echo "=========================================="
echo "🧪 Testing Email"
echo "=========================================="
echo ""

# Test the email
cd "$PROJECT_DIR"
source venv/bin/activate
python3 send_email_notification.py

echo ""
echo "=========================================="
echo "📧 Setup Complete!"
echo "=========================================="
echo ""
echo "Check your email: gianluca.veschi00@gmail.com"
echo ""
echo "If you didn't receive it:"
echo "  - Check spam folder"
echo "  - Verify app password is correct"
echo "  - See EMAIL_SETUP.md for troubleshooting"
echo ""
echo "✅ Email notifications will be sent after each bot run at 7 AM!"
echo ""

