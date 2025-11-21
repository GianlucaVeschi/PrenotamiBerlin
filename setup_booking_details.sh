#!/bin/bash
# Helper script to configure booking form details

echo "=========================================="
echo "📝 Booking Form Details Setup"
echo "=========================================="
echo ""
echo "This will add your personal details to .env"
echo "so the bot can automatically complete the booking form."
echo ""

PROJECT_DIR="/Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin"
ENV_FILE="${PROJECT_DIR}/.env"

# Check if .env exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ .env file not found!"
    echo "Please create it first with your Prenotami credentials"
    exit 1
fi

echo "Please provide the following information:"
echo ""

# Address
echo "1️⃣  Full residential address (required)"
echo "   Example: Via Roma 123, 00100 Roma RM, Italia"
read -p "   Address: " indirizzo

# Height
echo ""
echo "2️⃣  Height in centimeters (required)"
echo "   Example: 175"
read -p "   Height (cm): " statura

# Number of minor children
echo ""
echo "3️⃣  Number of minor children (default: 0)"
read -p "   Number: " figli
figli=${figli:-0}

# Notes (optional)
echo ""
echo "4️⃣  Notes for the office (optional, press Enter to skip)"
read -p "   Notes: " note

# Marital status (optional)
echo ""
echo "5️⃣  Marital status (optional, press Enter to skip)"
echo "   Options: Celibe/Nubile, Coniugato/a, Divorziato/a, Vedovo/a"
read -p "   Status: " stato_civile

echo ""
echo "=========================================="
echo "Summary:"
echo "=========================================="
echo "Address: $indirizzo"
echo "Height: $statura cm"
echo "Minor children: $figli"
echo "Notes: ${note:-<empty>}"
echo "Marital status: ${stato_civile:-<not specified>}"
echo ""
read -p "Is this correct? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 1
fi

# Add or update in .env
echo ""
echo "Updating .env file..."

# Remove existing booking details if any
sed -i '' '/^INDIRIZZO_RESIDENZA=/d' "$ENV_FILE"
sed -i '' '/^STATURA_CM=/d' "$ENV_FILE"
sed -i '' '/^NUMERO_FIGLI_MINORENNI=/d' "$ENV_FILE"
sed -i '' '/^NOTE_PER_SEDE=/d' "$ENV_FILE"
sed -i '' '/^TIPO_PRENOTAZIONE=/d' "$ENV_FILE"
sed -i '' '/^STATO_CIVILE=/d' "$ENV_FILE"

# Add new values
echo "" >> "$ENV_FILE"
echo "# Booking form details" >> "$ENV_FILE"
echo "INDIRIZZO_RESIDENZA=$indirizzo" >> "$ENV_FILE"
echo "STATURA_CM=$statura" >> "$ENV_FILE"
echo "NUMERO_FIGLI_MINORENNI=$figli" >> "$ENV_FILE"
echo "NOTE_PER_SEDE=$note" >> "$ENV_FILE"
echo "TIPO_PRENOTAZIONE=Prenotazione Singola" >> "$ENV_FILE"
echo "STATO_CIVILE=$stato_civile" >> "$ENV_FILE"

echo "✅ Booking details added to .env"
echo ""
echo "=========================================="
echo "🎉 Setup Complete!"
echo "=========================================="
echo ""
echo "The bot will now automatically:"
echo "  ✅ Find available slots"
echo "  ✅ Select a slot"
echo "  ✅ Fill in your details"
echo "  ✅ Accept privacy policy"
echo "  ✅ Submit the booking"
echo ""
echo "To test: python3 prenotami_bot.py"
echo ""

