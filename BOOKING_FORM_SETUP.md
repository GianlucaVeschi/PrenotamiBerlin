# 📝 Complete Booking Form Setup

The bot can now automatically complete the ENTIRE booking process, from login to final confirmation!

## 🎯 What the Bot Does Now

1. ✅ Logs into prenotami.esteri.it
2. ✅ Navigates to ID card booking
3. ✅ Finds available slots
4. ✅ Selects the first available slot
5. ✅ **Fills in your personal details**
6. ✅ **Accepts privacy policy**
7. ✅ **Clicks "Avanti" (Next)**
8. ✅ **Confirms the booking**
9. ✅ **Takes screenshots of everything**

## 🚀 Quick Setup

### Option 1: Interactive Setup (Easiest)

Run the setup helper:

```bash
~/VScodeProjects/PrenotamiBerlin/setup_booking_details.sh
```

It will ask you for:
- Your address
- Your height
- Number of minor children
- Notes (optional)
- Marital status (optional)

### Option 2: Manual Setup

Edit your `.env` file:

```bash
nano ~/VScodeProjects/PrenotamiBerlin/.env
```

Add these lines at the end:

```bash
# Booking form details
INDIRIZZO_RESIDENZA=Via Roma 123, 00100 Roma RM, Italia
STATURA_CM=175
NUMERO_FIGLI_MINORENNI=0
NOTE_PER_SEDE=
TIPO_PRENOTAZIONE=Prenotazione Singola
STATO_CIVILE=
```

## 📋 Field Details

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `INDIRIZZO_RESIDENZA` | Your complete residential address | `Via Roma 123, 00100 Roma RM, Italia` |
| `STATURA_CM` | Your height in centimeters (numbers only) | `175` |

### Optional Fields

| Field | Description | Default | Options |
|-------|-------------|---------|---------|
| `NUMERO_FIGLI_MINORENNI` | Number of minor children | `0` | Any number |
| `NOTE_PER_SEDE` | Notes for the office | Empty | Any text |
| `TIPO_PRENOTAZIONE` | Type of booking | `Prenotazione Singola` | From dropdown |
| `STATO_CIVILE` | Marital status | Empty | Celibe/Nubile, Coniugato/a, etc. |

## 🔄 Complete Flow

### What Happens When Bot Runs

```
7:00 AM → Cron triggers
├─ 1. Login ✅
├─ 2. Navigate to Prenota ✅
├─ 3. Click ID card booking ✅
├─ 4. Check for available slots
│   ├─ If NO slots → Exit (try again tomorrow)
│   └─ If YES slots ↓
├─ 5. Click first available slot ✅
├─ 6. Fill booking form with your details ✅
│   ├─ Select: Tipo di Prenotazione
│   ├─ Fill: Indirizzo completo di residenza
│   ├─ Fill: Statura in CM
│   ├─ Select: Stato Civile (if provided)
│   ├─ Fill: Numero figli minorenni
│   ├─ Fill: Note per la sede (if provided)
│   └─ Check: Privacy policy checkbox
├─ 7. Click "AVANTI" button ✅
├─ 8. Click "OK" on confirmation ✅
├─ 9. Take screenshots ✅
└─ 10. Send email notification ✅
```

## 📸 Screenshots Taken

The bot takes screenshots at every step:

1. `screenshot_login_*` - Login page
2. `screenshot_availability_page_*` - Slot availability
3. `screenshot_slot_selected_*` - After clicking a slot
4. `screenshot_booking_form_start_*` - Empty form
5. `screenshot_booking_form_filled_*` - Filled form
6. `screenshot_confirmation_page_*` - Confirmation dialog
7. `screenshot_booking_completed_*` - Final result

Check these to verify what happened!

## ✅ Verification

### Test Your Configuration

```bash
cd ~/VScodeProjects/PrenotamiBerlin
source venv/bin/activate

# This will check if all required fields are set
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()

required = ['INDIRIZZO_RESIDENZA', 'STATURA_CM']
for field in required:
    value = os.getenv(field)
    if value:
        print(f'✅ {field}: {value}')
    else:
        print(f'❌ {field}: NOT SET')
"
```

### What You Should See

```
✅ INDIRIZZO_RESIDENZA: Via Roma 123, 00100 Roma RM, Italia
✅ STATURA_CM: 175
```

If you see ❌, run the setup script again.

## 🧪 Test Run

To test without waiting for 7 AM:

```bash
cd ~/VScodeProjects/PrenotamiBerlin
source venv/bin/activate
python3 prenotami_bot.py
```

**Note:** This will attempt a REAL booking if slots are available!

## ⚠️ Important Notes

### Privacy Policy

The bot automatically checks the privacy policy checkbox:
> "Ho preso visione e accetto l'Informativa per la privacy"

### Tipo di Prenotazione

By default set to "Prenotazione Singola" (Single Booking).
If you need a different type, change it in `.env`.

### Stato Civile

This is optional. Leave empty if you don't want to specify.
Options include:
- Celibe/Nubile (Single)
- Coniugato/a (Married)
- Divorziato/a (Divorced)
- Vedovo/a (Widowed)

### Address Format

Use your FULL address as it appears on your documents:
```
Via/Viale/Piazza [Street Name] [Number], [Postal Code] [City] [Province], [Country]
```

Example:
```
Via Giuseppe Garibaldi 45, 10100 Torino TO, Italia
```

## 🔒 Security

All your personal information is stored in `.env` file which:
- ✅ Is in `.gitignore` (never committed to GitHub)
- ✅ Stays on your local computer only
- ✅ Is never shared or uploaded anywhere

## 🆘 Troubleshooting

### Bot stops at slot selection

**Problem:** You see `screenshot_booking_stopped_no_details_*.png`

**Solution:** Add your booking details to `.env`:
```bash
~/VScodeProjects/PrenotamiBerlin/setup_booking_details.sh
```

### Form fields not filling

**Problem:** Some fields remain empty in screenshots

**Cause:** Field IDs on the website might have changed

**Solution:** 
1. Check `screenshot_booking_form_filled_*` 
2. The bot logs warnings for fields it couldn't fill
3. May need to update field selectors in `prenotami_bot.py`

### Privacy checkbox not checked

**Problem:** Bot says it couldn't find privacy checkbox

**Solution:** Website structure may have changed. Check screenshot and update selector.

### Confirmation button not clicked

**Problem:** Bot stops at confirmation screen

**Cause:** Button text might be different

**Solution:** Bot looks for "OK", "CONFERMA", or "Conferma" - if it's different, update the code.

## 📊 What Gets Logged

Check the logs to see what happened:

```bash
tail -50 ~/VScodeProjects/PrenotamiBerlin/prenotami_bot.log
```

Look for:
```
✓ Selecting booking type: Prenotazione Singola
✓ Filling in address...
✓ Filling in height: 175 cm
✓ Accepting privacy policy...
✓ Privacy policy accepted
✓ Clicked 'Avanti'
✓ Clicked confirmation button!
🎉 Booking form submitted successfully!
```

## 🎉 Success Indicators

You know it worked if:
1. ✅ Log shows "Booking form submitted successfully!"
2. ✅ `screenshot_booking_completed_*` shows success message
3. ✅ You receive booking confirmation email from embassy
4. ✅ Booking appears in "I miei appuntamenti" on the website

## 🔄 After Successful Booking

1. **Check your email** - Embassy should send confirmation
2. **Log into prenotami.esteri.it** manually
3. **Go to "I miei appuntamenti"** - Your booking should be there
4. **Save the confirmation** - Screenshot or print

## 📝 Example .env File

Complete example:

```bash
# Prenotami login
EMAIL=gianluca.veschi00@gmail.com
PASSWORD=your_password_here

# Gmail notifications
GMAIL_APP_PASSWORD=your_app_password

# Booking form details
INDIRIZZO_RESIDENZA=Via Giuseppe Garibaldi 45, 10100 Torino TO, Italia
STATURA_CM=175
NUMERO_FIGLI_MINORENNI=0
NOTE_PER_SEDE=
TIPO_PRENOTAZIONE=Prenotazione Singola
STATO_CIVILE=Celibe/Nubile
```

## 🎯 Next Steps

1. **Set up booking details:**
   ```bash
   ~/VScodeProjects/PrenotamiBerlin/setup_booking_details.sh
   ```

2. **Test it:**
   ```bash
   cd ~/VScodeProjects/PrenotamiBerlin && source venv/bin/activate && python3 prenotami_bot.py
   ```

3. **Let it run automatically:**
   - The cron job is already set up
   - Bot will run at 7:00 AM
   - If a slot is found, it will complete the entire booking!

## ✅ Checklist

Before relying on the bot:

- [ ] Added all required fields to `.env`
- [ ] Tested the bot manually once
- [ ] Verified screenshots show filled form
- [ ] Checked logs for any warnings
- [ ] Cron job is active
- [ ] Email notifications configured (optional)
- [ ] Computer will be on at 7 AM

---

**You're all set! The bot will now handle the complete booking process automatically!** 🎉

