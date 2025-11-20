# 📧 Email Notifications Setup

Get email notifications after each bot run with the results!

## 🎯 What You'll Receive

After each bot run at 7:00 AM, you'll get an email with:
- ✅ Execution status (which day: 1/2/3)
- ✅ Slot availability status
- ✅ Number of screenshots created
- ✅ Last 20 lines of bot log
- ✅ Last 10 lines of cron log
- 🎉 **Alert if slot is found!**

## 📋 Setup Instructions

### Option 1: Gmail SMTP (Recommended)

#### Step 1: Enable 2-Factor Authentication on Gmail

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Under "Signing in to Google", click **2-Step Verification**
3. Follow the steps to enable it (if not already enabled)

#### Step 2: Create an App Password

1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Sign in if prompted
3. Under "Select app", choose **Mail**
4. Under "Select device", choose **Mac** (or Other)
5. Click **Generate**
6. **Copy the 16-character password** (example: `abcd efgh ijkl mnop`)

#### Step 3: Add to .env File

Edit your `.env` file:

```bash
nano /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin/.env
```

Add this line with your app password (remove spaces):

```bash
GMAIL_APP_PASSWORD=abcdefghijklmnop
```

Your complete `.env` should look like:

```bash
EMAIL=gianluca.veschi00@gmail.com
PASSWORD=your_prenotami_password
GMAIL_APP_PASSWORD=abcdefghijklmnop
```

Save and exit (Ctrl+X, then Y, then Enter)

#### Step 4: Test Email

```bash
cd /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin
source venv/bin/activate
python3 send_email_notification.py
```

Check your email (gianluca.veschi00@gmail.com) - you should receive a test email!

---

### Option 2: macOS Mail (Fallback)

If you don't want to use Gmail SMTP, you can use the built-in macOS Mail.app:

#### Requirements:
- Mail.app must be configured with your email account
- Must be able to send emails from Mail.app

#### Test:
```bash
echo "Test email body" | mail -s "Test Subject" gianluca.veschi00@gmail.com
```

If this works, the bot will automatically use this method if Gmail SMTP is not configured.

---

## ✅ Verification

### Test the Email System

Run a test email:

```bash
cd /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin
source venv/bin/activate
python3 send_email_notification.py
```

You should see:
```
✅ Email sent successfully to gianluca.veschi00@gmail.com
```

And receive an email within 1-2 minutes.

### Check Spam Folder

If you don't receive the email:
1. Check your **Spam** folder
2. Mark it as "Not Spam"
3. Add to your contacts

---

## 📧 Email Examples

### If No Slots Available

**Subject:** `Prenotami Bot Report - Day 1 of 3 - No slots yet`

**Body:**
```
📅 Date: Friday, November 21, 2025 at 07:05
📊 Status: Day 1 of 3

🎯 Slot Availability: No slots available (will try again tomorrow)
📸 Screenshots Created: 3

ℹ️  No slots available yet.
The bot will automatically run again tomorrow at 7:00 AM.
No action needed from you.
```

### If Slot Found! 🎉

**Subject:** `🎉 PRENOTAMI BOT: SLOT FOUND! - Action Required`

**Body:**
```
📅 Date: Friday, November 21, 2025 at 07:05
📊 Status: Day 1 of 3

🎯 Slot Availability: 🎉 AVAILABLE SLOT FOUND!
📸 Screenshots Created: 4

🚨 ACTION REQUIRED! 🚨

AN APPOINTMENT SLOT WAS FOUND!

Next Steps:
1. Log into: https://prenotami.esteri.it/
2. Navigate to Prenota → ID Card booking
3. Complete the booking IMMEDIATELY!
4. Check screenshots in the project folder for details

Time is critical - act now!
```

---

## 🔧 Troubleshooting

### "Gmail app password not configured"

**Problem:** `.env` file doesn't have `GMAIL_APP_PASSWORD`

**Solution:**
1. Create Gmail App Password (see Step 2 above)
2. Add to `.env` file
3. Test again

### "Failed to send email"

**Problem:** Incorrect app password or network issue

**Solutions:**
1. Verify app password is correct (16 characters, no spaces)
2. Check internet connection
3. Verify 2FA is enabled on Google account
4. Try regenerating the app password

### "Username and Password not accepted"

**Problem:** Using regular Gmail password instead of app password

**Solution:** You **must** use an App Password, not your regular Gmail password

### Email Goes to Spam

**Solution:**
1. Check spam folder
2. Mark as "Not Spam"
3. Add sender to contacts
4. Create a filter in Gmail to always mark as important

---

## 🔒 Security Notes

### App Password vs Regular Password

- ✅ **App Password** - Specific to this application, can be revoked anytime
- ❌ **Regular Password** - Won't work with SMTP, less secure

### Revoking Access

To revoke email access:
1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Find "Mail - Mac" (or whatever you named it)
3. Click **Remove**

The bot will stop sending emails but will continue to run normally.

---

## 📱 Mobile Notifications

To get push notifications on your phone:

1. Ensure Gmail app is installed
2. Enable notifications for Gmail
3. Set as high priority/important
4. You'll get instant alerts when emails arrive!

**Even better:** Create a Gmail filter to:
- Star emails from this bot
- Mark as important
- Never send to spam
- Play a sound notification

---

## ⚙️ Advanced: Customize Email

Edit the email script:

```bash
nano /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin/send_email_notification.py
```

You can modify:
- Subject line format
- Email body content
- What information is included
- Recipient email address

---

## 🧪 Test Commands

### Test email with current bot status:
```bash
cd ~/VScodeProjects/PrenotamiBerlin
source venv/bin/activate
python3 send_email_notification.py
```

### Check if email credentials are loaded:
```bash
cd ~/VScodeProjects/PrenotamiBerlin
source venv/bin/activate
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Gmail password configured!' if os.getenv('GMAIL_APP_PASSWORD') else 'Not configured')"
```

---

## 📊 What Gets Sent

Every email includes:
1. **Execution Summary**
   - Date and time
   - Current day (1/2/3)
   - Slot status
   - Screenshot count

2. **Cron Log** (last 10 lines)
   - When the job ran
   - Which day it is

3. **Bot Log** (last 20 lines)
   - Login status
   - Navigation steps
   - Any errors

4. **Action Items**
   - What to do next
   - Urgency level

---

## 🎯 Next Steps

1. **Set up App Password** (5 minutes)
2. **Add to `.env` file** (1 minute)
3. **Test email** (1 minute)
4. **Done!** You'll get emails automatically starting tomorrow at 7 AM

---

## 💡 Pro Tips

- **Enable Gmail notifications** on your phone
- **Create a Gmail filter** for these emails
- **Check spam folder** on first email
- **Set as important** so you don't miss slot alerts
- **Test before tomorrow** to ensure it works

---

## ✅ Checklist

- [ ] 2-Factor Authentication enabled on Gmail
- [ ] App Password created
- [ ] App Password added to `.env` file
- [ ] Test email sent and received
- [ ] Email marked as "Not Spam"
- [ ] Gmail notifications enabled on phone

---

**Once set up, you'll automatically receive email updates after each bot run!**

No need to manually check logs or screenshots - it all comes to your inbox! 📧

