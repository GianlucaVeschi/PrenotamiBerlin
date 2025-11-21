# 🎉 Complete Setup Guide - Prenotami Bot

## ✅ What's Been Built

A **fully automated bot** that:
1. ✅ Logs into prenotami.esteri.it
2. ✅ Finds available ID card appointment slots
3. ✅ Selects the first available slot
4. ✅ **Fills in your personal details automatically**
5. ✅ **Accepts privacy policy**
6. ✅ **Submits the booking form**
7. ✅ **Confirms the booking**
8. ✅ Takes screenshots of everything
9. ✅ Sends email notifications
10. ✅ Runs automatically at 7 AM daily

---

## 🚀 Quick Start (5 Steps)

### Step 1: Configure Login & Booking Details

```bash
cd ~/VScodeProjects/PrenotamiBerlin

# Option A: Interactive setup (easiest)
./setup_booking_details.sh

# Option B: Manual setup
nano .env
```

Your `.env` should contain:

```bash
# Login credentials
EMAIL=your@email.com
PASSWORD=your_prenotami_password

# Booking form details
INDIRIZZO_RESIDENZA=Via Roma 123, 00100 Roma RM, Italia
STATURA_CM=175
NUMERO_FIGLI_MINORENNI=0
NOTE_PER_SEDE=
TIPO_PRENOTAZIONE=Prenotazione Singola
STATO_CIVILE=

# Email notifications (optional but recommended)
GMAIL_APP_PASSWORD=your_gmail_app_password
```

### Step 2: Verify Configuration

```bash
~/VScodeProjects/PrenotamiBerlin/check_bot_status.sh
```

### Step 3: Test the Bot (Optional but Recommended)

```bash
cd ~/VScodeProjects/PrenotamiBerlin
source venv/bin/activate
python3 prenotami_bot.py
```

⚠️ **Warning:** This will make a real booking if slots are available!

### Step 4: Verify Cron Job is Running

```bash
crontab -l
```

You should see:
```
0 7 * * * /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin/run_bot_with_limit.sh
```

### Step 5: Done! 🎉

The bot will now run automatically at 7 AM and complete the entire booking if slots are found!

---

## 📋 Configuration Files

### Required: `.env`

Contains all your credentials and personal details.

**Get the template:**
```bash
cp ~/VScodeProjects/PrenotamiBerlin/env.example ~/.env
```

**Fields:**

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `EMAIL` | ✅ Yes | Prenotami login | `your@email.com` |
| `PASSWORD` | ✅ Yes | Prenotami password | `yourpassword` |
| `INDIRIZZO_RESIDENZA` | ✅ Yes | Full address | `Via Roma 123, 00100 Roma RM` |
| `STATURA_CM` | ✅ Yes | Height in cm | `175` |
| `NUMERO_FIGLI_MINORENNI` | No | Minor children | `0` |
| `NOTE_PER_SEDE` | No | Notes | (empty) |
| `TIPO_PRENOTAZIONE` | No | Booking type | `Prenotazione Singola` |
| `STATO_CIVILE` | No | Marital status | (empty) |
| `GMAIL_APP_PASSWORD` | Recommended | For emails | App password from Google |

---

## 📊 What Happens Daily

```
7:00 AM Daily
    ↓
🤖 Bot starts
    ↓
1️⃣ Login to prenotami.esteri.it ✅
    ↓
2️⃣ Navigate to ID card booking ✅
    ↓
3️⃣ Check for available slots
    ↓
    ├─ NO SLOTS FOUND
    │   ├─ Log: "No slots available"
    │   ├─ Take screenshot
    │   ├─ Send email (no action needed)
    │   └─ Exit (try again tomorrow)
    │
    └─ SLOT FOUND! 🎉
        ↓
    4️⃣ Click on first available slot ✅
        ↓
    5️⃣ Fill booking form ✅
        ├─ Tipo di Prenotazione
        ├─ Indirizzo residenza
        ├─ Statura (height)
        ├─ Stato civile (if provided)
        ├─ Numero figli
        └─ Note (if provided)
        ↓
    6️⃣ Accept privacy policy ✅
        ↓
    7️⃣ Click "AVANTI" ✅
        ↓
    8️⃣ Click "OK" to confirm ✅
        ↓
    9️⃣ Take screenshots ✅
        ↓
    🔟 Send urgent email alert ✅
        ↓
    ✅ BOOKING COMPLETE!
```

---

## 📸 Screenshots Generated

Every step is documented:

| Screenshot | When | What it shows |
|------------|------|---------------|
| `screenshot_login_*` | After login | Login page |
| `screenshot_availability_page_*` | Checking slots | Available dates |
| `screenshot_slot_selected_*` | After clicking slot | Selected time |
| `screenshot_booking_form_start_*` | Form appears | Empty form |
| `screenshot_booking_form_filled_*` | After filling | Completed form |
| `screenshot_confirmation_page_*` | Before confirming | Confirmation dialog |
| `screenshot_booking_completed_*` | Final step | Success/result page |

**Location:** `~/VScodeProjects/PrenotamiBerlin/screenshot_*.png`

---

## 📧 Email Notifications

After each run, you receive an email with:
- ✅ Execution status
- ✅ Day counter (1/2/3)
- ✅ Slot availability
- ✅ Screenshot count
- ✅ Recent logs

**If slot found:** 🚨 **URGENT email with action alert**

### Setup Email Notifications

1. Enable 2FA: https://myaccount.google.com/security
2. Create app password: https://myaccount.google.com/apppasswords
3. Add to `.env`: `GMAIL_APP_PASSWORD=your_app_password`
4. Test: `~/VScodeProjects/PrenotamiBerlin/debug_email.sh`

---

## 🔍 Monitoring & Debugging

### Quick Check: Did it run today?

```bash
~/VScodeProjects/PrenotamiBerlin/did_it_run.sh
```

### Detailed Status

```bash
~/VScodeProjects/PrenotamiBerlin/check_bot_status.sh
```

### View Logs

```bash
# Cron execution log
tail -50 ~/VScodeProjects/PrenotamiBerlin/cron_bot.log

# Bot activity log
tail -50 ~/VScodeProjects/PrenotamiBerlin/prenotami_bot.log
```

### Debug Email

```bash
~/VScodeProjects/PrenotamiBerlin/debug_email.sh
```

### Test Mail System

```bash
~/VScodeProjects/PrenotamiBerlin/test_mail.sh
```

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **README.md** | Main documentation |
| **QUICK_START.md** | Getting started guide |
| **STATUS.md** | Current status and test results |
| **CRON_SETUP.md** | Cron job configuration |
| **EMAIL_SETUP.md** | Email notification setup |
| **BOOKING_FORM_SETUP.md** | Form automation details |
| **TROUBLESHOOTING.md** | Common issues and solutions |
| **MORNING_CHECKLIST.md** | Daily monitoring guide |

---

## 🛠️ Helper Scripts

| Script | Purpose |
|--------|---------|
| `setup_booking_details.sh` | Configure booking form details |
| `setup_email.sh` | Configure email notifications |
| `check_bot_status.sh` | Check if bot ran successfully |
| `did_it_run.sh` | Quick check for today's run |
| `debug_email.sh` | Troubleshoot email issues |
| `test_mail.sh` | Test mail configuration |
| `run_scheduler.sh` | Start unlimited scheduler |
| `run_bot_with_limit.sh` | Run with 3-day limit (used by cron) |

---

## ⚙️ Advanced Configuration

### Change Schedule

Edit crontab:
```bash
crontab -e
```

Change from 7 AM to different time:
```
0 8 * * *  # 8 AM
0 6 * * *  # 6 AM
*/5 7 * * *  # Every 5 minutes during 7 AM hour
```

### Extend Beyond 3 Days

Edit `run_bot_with_limit.sh`:
```bash
nano ~/VScodeProjects/PrenotamiBerlin/run_bot_with_limit.sh
```

Change:
```bash
DAYS_TO_RUN=3  # Change to any number
```

### Run Headless (No Browser Window)

Edit `prenotami_bot.py` main function:
```python
bot = PrenotamiBot(..., headless=True)
```

---

## 🔒 Security

✅ **All personal data stored locally**
- `.env` file never committed to Git
- Listed in `.gitignore`
- Never uploaded anywhere

✅ **No data sent to third parties**
- Bot runs entirely on your computer
- Only connects to prenotami.esteri.it and Gmail

✅ **Gmail app password**
- Specific to this application
- Can be revoked anytime
- Doesn't expose your main password

---

## ✅ Pre-Flight Checklist

Before relying on the bot:

- [ ] `.env` file configured with all required fields
- [ ] Booking details added (address, height)
- [ ] Email notifications configured (recommended)
- [ ] Tested bot manually once
- [ ] Reviewed screenshots from test run
- [ ] Cron job is active (`crontab -l`)
- [ ] Computer will be on at 7 AM
- [ ] Computer will NOT be asleep at 7 AM

---

## 🎯 Success Criteria

You'll know it worked when:

1. ✅ Log shows "Booking form submitted successfully!"
2. ✅ Screenshot `booking_completed_*` shows success
3. ✅ Email received with urgent alert
4. ✅ Booking confirmation from embassy
5. ✅ Booking appears in "I miei appuntamenti"

---

## 🆘 Troubleshooting

### Bot didn't run

**Check:**
```bash
# Verify cron job exists
crontab -l

# Check if computer was awake
pmset -g log | grep -i sleep

# Check logs
tail -20 ~/VScodeProjects/PrenotamiBerlin/cron_bot.log
```

### Form not filling

**Check:**
```bash
# Verify booking details are set
grep "INDIRIZZO_RESIDENZA" ~/VScodeProjects/PrenotamiBerlin/.env

# Run debug
~/VScodeProjects/PrenotamiBerlin/check_bot_status.sh
```

### Email not received

```bash
# Debug email system
~/VScodeProjects/PrenotamiBerlin/debug_email.sh

# Check spam folder
# Verify Gmail app password is correct
```

---

## 📞 Support

### Check Documentation

All guides are in the project folder:
```bash
cd ~/VScodeProjects/PrenotamiBerlin
ls *.md
```

### View Logs

```bash
# See what happened
tail -100 ~/VScodeProjects/PrenotamiBerlin/prenotami_bot.log

# Cron execution
tail -50 ~/VScodeProjects/PrenotamiBerlin/cron_bot.log
```

### GitHub Repository

https://github.com/GianlucaVeschi/PrenotamiBerlin

---

## 🎉 You're All Set!

The bot is now **fully automated** and will:
- ✅ Run daily at 7 AM
- ✅ Find available slots
- ✅ **Complete the entire booking automatically**
- ✅ Send you notifications
- ✅ Stop after 3 days (or extend as needed)

**No manual intervention needed!**

Just check your email each morning or run:
```bash
~/VScodeProjects/PrenotamiBerlin/did_it_run.sh
```

---

**Good luck booking your appointment!** 🍀 🇮🇹 🎉

